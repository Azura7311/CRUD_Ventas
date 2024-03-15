from django.contrib.auth import authenticate, login,logout
from django.http import FileResponse
from django.shortcuts import render,redirect
from django.contrib import messages
from .models import *
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
from reportlab.pdfgen import canvas
import random, io

# Información para las ventas

lista_productos = []
info_usuario = {}
total = 0

def home(request):
    # Sistema de login
    request.session["list"] = []
    if request.method == "POST":
        # Obtener datos usuario
        username = request.POST.get("nombre")
        email = request.POST.get("email")
        password = request.POST.get("password")
        # Autenticar y verificar que existe
        user = authenticate(username=username,email=email, password=password)
        try:
            e= User.objects.get(username = username)
        except ObjectDoesNotExist:
            return render(request, 'index.html')

        if user is not None and e.email == email:
            login(request, user)
            number_list = [x for x in range(10)]
            code_items = []
            # Generar codigo de autenticación
            for y in range(5):
                num = random.choice(number_list)
                code_items.append(num)
            code_string = "".join(str(item) for item in code_items)
            # Enviar correo con el código
            send_mail("Email Verification",
                      f"""Your code: {code_string} """,
                      "lll737965@gmail.com",
                      (str(email), None),
                      fail_silently=False
                      )
            global val
            def val():
                return code_string
            return redirect("autenticador")
        else:
            messages.error(request, "Try again")
            return render(request, 'index.html')
    return render(request, 'index.html')

def autenticador(request):
    if request.method == "POST":
        code_string= val()
        code = request.POST["autenticador"]
        print(code_string)
        if code == code_string:
            return redirect('dashboard')
        else :
            return redirect('home')
    return render(request, 'autenticador.html')

def dashboard(request):
    # Verificar logout
    if request.method == "POST":
        if "logout" in request.POST:
            logout(request)
            return redirect("home")
        else:
            pass
    return render(request, 'dashboard.html')

def registro_ventas_1(request):
    # Verificar logout
    if request.method == "POST":
        if "logout" in request.POST:
            logout(request)
            return redirect("home")
        else:
            pass
    context = get_context()
    return render(request, 'registro_ventas_1.html', context)

def registro_ventas_2(request):
    # Verificar logout
    if request.method == "POST":
        if "logout" in request.POST:
            logout(request)
            return redirect("home")
        else:
            pass
    return render(request, 'registro_ventas_2.html')

def reporte_ventas(request):
    # Si no es admin no puede entrar a la pagina
    if not request.user.is_superuser:
        return render(request, 'dashboard.html')
    # Verificar logout
    if request.method == "POST":
        if "logout" in request.POST:
            logout(request)
            return redirect("home")
        else:
            pass
    # Obtener rango de fechas
    a = request.POST
    desde = a.get("desde")
    hasta = a.get("hasta")
    ventas = {}
    # Buscar en la base de datos las ventas correctas
    if desde != None and hasta != None:
        ventas = Recibo.objects.raw(f'SELECT * FROM home_Recibo WHERE fecha BETWEEN date("{desde}") AND date("{hasta}")')
    context = {'ventas' : ventas}
    return render(request, 'reporte_ventas.html', context)

def comisiones(request):
    if not request.user.is_superuser:
        return render(request, 'dashboard.html')
    if request.method == "POST":
        if "logout" in request.POST:
            logout(request)
            return redirect("home")
        else:
            pass
    a = request.POST
    # Obtener rango de fechas
    desde = a.get("desde")
    hasta = a.get("hasta")
    ventas = {}
    # Buscar en la base de datos las comisiones
    if desde != None and hasta != None:
        ventas = Recibo.objects.raw(f'SELECT * FROM home_Recibo WHERE fecha BETWEEN date("{desde}") AND date("{hasta}")')
    context = {'ventas' : ventas}
    return render(request, 'comisiones.html', context)

def buscar_producto(id):
    # Buscar producto en la lista de compra actual
    i = 0
    while i < len(lista_productos) and lista_productos[i][0].id != id:
        i += 1
    return i

def get_context():
    # Organizar información para mostrar en el front del registro de ventas
    global total
    total = 0
    for i in lista_productos:
        i[2] = i[1] * int(i[0].precio)
        total += i[2]
        print(total)
    context = {'lista_productos' : lista_productos, 'total' : total}
    return context

def agregar_producto(request):
    # Agregar producto a la lista de compras
    form = request.POST.get('producto_id')
    p = Producto.objects.raw(f'SELECT * FROM home_Producto where id="{form}"')
    if len(p) > 0:
        if p[0].inventario > 1:
            i = buscar_producto(p[0].id)
            if i == len(lista_productos):
                lista_productos.append([p[0], 1, 0])
            else:
                # Si ya se encuentra en la lista, agregar 1 cantidad
                lista_productos[i][1] += 1
    context = get_context()
    return render(request, 'registro_ventas_1.html', context)

def borrar_producto(request):
    # Borrar producto de la lista de compras
    a = request.POST.get("id")
    i = buscar_producto(a)
    if i < len(lista_productos):
        lista_productos.pop(i)
    context = get_context()
    return render(request, 'registro_ventas_1.html', context)

def cantidad_producto(request):
    # Modificar cantidad de un producto ya agregado
    a = request.POST
    id = a.get('id')
    i = buscar_producto(id)
    p = Producto.objects.raw(f'SELECT * FROM home_Producto where id="{id}"')
    # Solo agrega cantidad si se cuenta con el inventario suficiente
    if p[0].inventario >= int(a.get('cantidad')):
        lista_productos[i][1] = int(a.get('cantidad'))
    context = get_context()
    return render(request, 'registro_ventas_1.html', context)
    
def registrar_venta(request):
    # Confirmar y registrar la venta en la base de datos
    global total, lista_productos
    a = request.POST
    info_usuario["id"] = a.get("id")
    info_usuario["nombre"] = a.get("nombre")
    info_usuario["email"] = a.get("email")
    info_usuario["metodo_pago"] = a.get("metodo")
    info_usuario["monto"] = a.get("monto")
    recibo = Recibo()
    recibo.id_cliente = info_usuario["id"]
    recibo.cliente = info_usuario["nombre"]
    recibo.email = info_usuario["email"]
    recibo.metodo_pago = info_usuario["metodo_pago"]
    recibo.monto = info_usuario["monto"]
    recibo.total = total
    recibo.num_productos = 0
    recibo.save()
    num_productos = 0
    for i in lista_productos:
        i[0].inventario -= i[1]
        i[0].save()
        compra = Compra(recibo=recibo.id, producto_id=i[0].id, cantidad=i[1], total=i[2])
        compra.save()
        num_productos += i[1]
    lista_productos = []
    total = 0
    recibo.num_productos = num_productos
    recibo.save()
    context = {'id' : recibo.id}
    return render(request, 'registro_ventas_3.html', context)

def detalle_ventas(request):
    id = request.POST.get("id")
    context = {'compras' : []}
    compras = Compra.objects.raw(f'SELECT * FROM home_Compra WHERE recibo="{id}"')
    
    # Esto se puede hacer con un JOIN, pero django por alguna razón no lo permitió
    for i in compras:
        compra = {}
        producto = Producto.objects.raw(f'SELECT * FROM home_Producto WHERE id="{i.producto_id}"')
        compra['id'] = producto[0].id
        compra['producto'] = producto[0].nombre
        compra['precio'] = producto[0].precio
        compra['cantidad'] = i.cantidad
        compra['total'] = i.total
        context['compras'].append(compra)
    context['total'] = Recibo.objects.raw(f'SELECT * FROM home_Recibo WHERE id="{id}"')[0].total
    context['id'] = id
    return render(request, 'detalle_ventas.html', context)

def imprimir_recibo(request):
    # Generar pdf con recibo para imprimir
    id = request.POST.get('id')
    recibo = Recibo.objects.raw(f'SELECT * FROM home_Recibo WHERE id="{id}"')[0]
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)
    x = 70
    y = 750
    p.drawString(x, y, f'Recibo venta #{id}')
    p.drawString(x, y - 50, f'Producto')
    p.drawString(x + 125, y - 50, f'Cantidad')
    p.drawString(x + 250, y - 50, f'Valor Unitario')
    p.drawString(x + 375, y - 50, f'Total')
    compras = Compra.objects.raw(f'SELECT * FROM home_Compra WHERE recibo="{id}"')
    y -= 100
    for i in compras:
        producto = Producto.objects.raw(f'SELECT * FROM home_Producto WHERE id="{i.producto_id}"')[0]
        p.drawString(x, y, f'{producto.nombre}')
        p.drawString(x + 125, y, f'{i.cantidad}')
        p.drawString(x + 250, y, f'{producto.precio}')
        p.drawString(x + 375, y, f'{i.total}')
        y -= 25
    p.drawString(x, y - 50, f'Total: {recibo.total}')
    p.drawString(x, y - 75, f'Recibido: {recibo.monto}')
    p.drawString(x, y - 100, f'Cambio: {recibo.monto - recibo.total}')
    y -= 200
    p.drawString(x, y, f'Cliente: {recibo.cliente}')
    p.drawString(x, y - 25, f'Correo: {recibo.email}')
    p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename="hello.pdf")

def agregar_inventario(request):
    # Agregar / Actualizar producto a la base de datos
    if not request.user.is_superuser:
        return render(request, 'dashboard.html')
    a = request.POST
    context = {}
    if a:
        producto = Producto.objects.raw(f'SELECT * FROM home_Producto WHERE id="{a.get("id")}"')
        if len(list(producto)) > 0:
            producto = producto[0]
            if a.get("nombre"):
                producto.nombre = a.get("nombre")
            if a.get("precio"):
                producto.precio = a.get("precio")
            if a.get("cantidad"):
                producto.inventario += int(a.get("cantidad"))
            producto.save()
        else:
            producto = Producto(id=a.get("id"), nombre=a.get("nombre"), precio=a.get("precio"), inventario=int(a.get("cantidad")))
            producto.save()
        context['producto'] = producto
    return render(request, 'agregar_inventario.html', context)