from django.shortcuts import render, redirect, get_object_or_404
from .models import Transacao, Investimento
from django.db.models import Sum, Q
from django.db.models.functions import TruncMonth

def dashboard(request):
    # ----------------------------------------------------
    # 1. PROCESSAMENTO DE AÇÕES (INSERIR / EDITAR / DELETAR)
    # ----------------------------------------------------
    acao = request.POST.get('acao')
    
    if request.method == 'POST' and acao:
        # --- AÇÕES PARA TRANSAÇÕES ---
        if acao == 'salvar_transacao':
            id_transacao = request.POST.get('id')
            if id_transacao: 
                t = get_object_or_404(Transacao, pk=id_transacao)
            else: 
                t = Transacao()
            t.item = request.POST.get('item')
            t.valor = request.POST.get('valor')
            t.data = request.POST.get('data')
            t.tipo = request.POST.get('tipo')
            t.save()
            return redirect('dashboard')

        elif acao == 'deletar_transacao':
            id_transacao = request.POST.get('id')
            t = get_object_or_404(Transacao, pk=id_transacao)
            t.delete()
            return redirect('dashboard')

        # --- AÇÕES PARA INVESTIMENTOS ---
        elif acao == 'salvar_investimento':
            id_investimento = request.POST.get('id')
            if id_investimento: 
                i = get_object_or_404(Investimento, pk=id_investimento)
            else: 
                i = Investimento()
            i.item = request.POST.get('item')
            i.valor = request.POST.get('valor')
            i.data = request.POST.get('data')
            i.tipo = request.POST.get('tipo')
            i.save()
            return redirect('dashboard')

        elif acao == 'deletar_investimento':
            id_investimento = request.POST.get('id')
            i = get_object_or_404(Investimento, pk=id_investimento)
            i.delete()
            return redirect('dashboard')

    # ----------------------------------------------------
    # 2. CAPTURA DE DADOS PARA EDIÇÃO (PREENCHER FORMULÁRIO)
    # ----------------------------------------------------
    edit_transacao = None
    edit_investimento = None
    
    if request.method == 'GET':
        edit_t_id = request.GET.get('edit_t')
        edit_i_id = request.GET.get('edit_i')
        if edit_t_id:
            edit_transacao = get_object_or_404(Transacao, pk=edit_t_id)
        if edit_i_id:
            edit_investimento = get_object_or_404(Investimento, pk=edit_i_id)

    # ----------------------------------------------------
    # 3. FILTROS POR DATA, ITEM E RENDERIZAÇÃO PADRÃO
    # ----------------------------------------------------
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')
    pesquisa = request.GET.get('pesquisa')
    
    transacoes_query = Transacao.objects.all()
    investimentos_query = Investimento.objects.all()
    
    if pesquisa:
        transacoes_query = transacoes_query.filter(item__icontains=pesquisa)
        investimentos_query = investimentos_query.filter(item__icontains=pesquisa)

    if data_inicio:
        transacoes_query = transacoes_query.filter(data__gte=data_inicio)
        investimentos_query = investimentos_query.filter(data__gte=data_inicio)
    if data_fim:
        transacoes_query = transacoes_query.filter(data__lte=data_fim)
        investimentos_query = investimentos_query.filter(data__lte=data_fim)
        
    transacoes = transacoes_query.order_by('codigo')
    investimentos = investimentos_query.order_by('codigo')
    
    total_receitas = transacoes.filter(tipo='RECEITA').aggregate(Sum('valor'))['valor__sum'] or 0
    total_despesas = transacoes.filter(tipo='DESPESA').aggregate(Sum('valor'))['valor__sum'] or 0
    total_ativos = investimentos.filter(tipo='ATIVO').aggregate(Sum('valor'))['valor__sum'] or 0
    total_passivos = investimentos.filter(tipo='PASSIVO').aggregate(Sum('valor'))['valor__sum'] or 0
    
    despesa_geral = total_despesas + total_ativos
    balanco_geral = total_receitas - despesa_geral

    # --- HISTÓRICO MENSAL PARA O GRÁFICO DE LINHAS ---
    historico_mensal = (
        transacoes_query
        .annotate(mes=TruncMonth('data'))
        .values('mes')
        .annotate(
            receitas_mes=Sum('valor', filter=Q(tipo='RECEITA')),
            despesas_mes=Sum('valor', filter=Q(tipo='DESPESA'))
        )
        .order_by('mes')
    )

    labels_meses = []
    dados_receitas = []
    dados_despesas = []

    for registro in historico_mensal:
        if registro['mes']:
            nome_mes = registro['mes'].strftime('%m/%Y')
            labels_meses.append(nome_mes)
            dados_receitas.append(float(registro['receitas_mes'] or 0))
            dados_despesas.append(float(registro['despesas_mes'] or 0))
    
    dados = {
        'transacoes': transacoes,
        'investimentos': investimentos,
        'total_receitas': total_receitas,
        'total_despesas': total_despesas,
        'total_ativos': total_ativos,
        'total_passivos': total_passivos,
        'despesa_geral': despesa_geral,
        'balanco_geral': balanco_geral,
        'data_inicio': data_inicio,
        'data_fim': data_fim,
        'pesquisa': pesquisa,
        'edit_transacao': edit_transacao,
        'edit_investimento': edit_investimento,
        'labels_meses': labels_meses,
        'dados_receitas': dados_receitas,
        'dados_despesas': dados_despesas,
    }
    
    return render(request, 'fluxo/dashboard.html', dados)
