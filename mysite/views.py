from django.shortcuts import render,redirect
from loja.models import Produtos, Carrinho,Clientes
from random import choice
import string
from django.http import HttpResponseRedirect
from django.db.models import Sum, Min
from django.utils.formats import localize


def home(request):
 produtos = Produtos.objects.filter(promocao=0)
 
 if not request.session.get('chave'):
   string.ascii_lowercase # abcdefghijklmnopqrstuvwxyz
   string.ascii_uppercase # ABCDEFGHIJKLMNOPQRSTUVWXYZ
   tam = 10
   valores = string.ascii_lowercase + string.ascii_uppercase
   chave = ''
   for i in range(10):
     chave += choice(valores)
   request.session['chave'] = chave
 cha = request.session['chave']
 #contar carrinho
 total = Carrinho.objects.filter(chave=cha).count()
 context = {
 'produtos': produtos,
 'total':total
 }
 return render(request, 'index.html', context)
 

def addCart(request,pk):
 carrinho = Carrinho()
 produtos = Produtos.objects.get(pk=pk)
 carrinho.chave = request.session['chave']
 carrinho.pedido = produtos.nome
 carrinho.valor = produtos.valor
 carrinho.qtd = 1
 carrinho.save()

 #carrinhos = Carrinho.objects.all()
 cha = request.session['chave']
 #contar carrinho
 total = Carrinho.objects.filter(chave=cha).count()

 carrinhos = Carrinho.objects.filter(chave=cha)

 somar =  Carrinho.objects.filter(chave=cha).aggregate(Sum('valor'))
 somar = somar.get('valor__sum')
 produtos = Produtos.objects.filter(promocao=0)
 context = {
 'carrinho': carrinhos,
 'msg':'Inserido com sucesso!',
 'total':total,
 'somar':somar,
 'produtos': produtos,
 }
 return redirect('home')# render(request, 'index.html', context)

def verCar(request):
 cha = request.session['chave']
 #carrinhos = Carrinho.objects.all()
 carrinhos = Carrinho.objects.filter(chave=cha)
 somar =  Carrinho.objects.filter(chave=cha).aggregate(Sum('valor'))
 somar = somar.get('valor__sum')

 #contar carrinho
 total = Carrinho.objects.filter(chave=cha).count()

 context = {
 'carrinho': carrinhos,
 'msg':'Carrinho de compras',
 'somar':somar,
 'total':total
 }
 return render(request, 'carrinho.html', context)


def detail(request,pk):
 produtos = Produtos.objects.get(pk=pk)
    #contar carrinho
 cha = request.session['chave']
 total = Carrinho.objects.filter(chave=cha).count()
 context = {
 'total':total,  
 'produtos': produtos
 }
 return render(request, 'detalhes.html', context)


def cadcli(request):
  #cad clientes
  cli = Clientes()
  chave = request.session['chave']

  pedido =  chave
  nome =  request.POST['your_name']
  pagamento =  request.POST['pagamento']
  endereco =  request.POST['endereco']
  cli.nome = nome
  cli.pedido = pedido
  cli.pagamento = pagamento
  cli.endereco=endereco
  cli.save()


  context = {
   
   }
  return render(request, 'cadcliconfirmar.html', context)


def cadclichama(request):
     #contar carrinho

  context = {
   
   }
  return render(request, 'cadcli.html', context)


def excpedido(request,pk):
  carrinho = Carrinho.objects.get(pk=pk).delete()
  cha = request.session['chave']
 #carrinhos = Carrinho.objects.all()
  carrinhos = Carrinho.objects.filter(chave=cha)
 #contar carrinho
  total = Carrinho.objects.filter(chave=cha).count()
  somar =  Carrinho.objects.filter(chave=cha).aggregate(Sum('valor'))
  somar = somar.get('valor__sum')
  context = {
   'carrinho': carrinhos,
   'total': total,
   'somar':somar
   }
  return render(request, 'carrinho.html', context)

def enviar(request):
  #enviar pedido
  cha = request.session['chave']
  carrinhos = Carrinho.objects.filter(chave=cha)
  clientes = Clientes.objects.filter(pedido=cha)

  somar =  Carrinho.objects.filter(chave=cha).aggregate(Sum('valor'))
  somar = str(somar.get('valor__sum'))
   ##serialize
  output=[]
 
  output.append("Pedido: "+cha)
  for cli in clientes:
      output.append("Nome: "+cli.nome)
      output.append("endereço: "+cli.endereco)
  
  output.append("produtos: " )

  for dados in carrinhos:
    output.append(dados.pedido)
    output.append(dados.valor)
  output.append("Total: R$"+ somar)
  #print(output)
  #print('\n'.join(map(str, output)))
  #formata a saída sem aspas
  output='\n'.join(map(str, output))
  del request.session['chave']        
  return HttpResponseRedirect("https://api.whatsapp.com/send?phone=" + "55"+"91983185630" + "&text=" + str(output),"_blank")


def moeda(request):
  valor = 1768 
  valor = localize(valor)
  return ('Valor: %s' % valor)

