// JAVASCRIPT PARA PÁGINA HOME DO ADMINISTRATIVO

// BLOQUEIA QUE O USUARIO VOLTE PARA LOGIN/CADASTRO APÓS AUTENTICAÇÃO
if (window.history && window.history.pushState) {
    window.history.pushState(null, null, window.location.href);
    window.onpopstate = function() {
        window.history.pushState(null, null, window.location.href);
    };
}

// FUNÇÃO PARA ABRIR MODAL DE EDIÇÃO
function abrirModalEditar(id, titulo, descricao) {
    console.log('Abrindo modal de edição para receita:', id);
    document.getElementById('edit_receita_id').value = id;
    document.getElementById('edit_titulo').value = titulo;
    document.getElementById('edit_descricao').value = descricao;
    
    // Atualizar action do formulário
    const editUrl = document.getElementById('formEditarReceita').dataset.editUrl;
    document.getElementById('formEditarReceita').action = editUrl.replace('0', id);
    
    // Abrir modal
    var modalElement = document.getElementById('modalEditarReceita');
    var modal = new bootstrap.Modal(modalElement);
    modal.show();
}

// FUNÇÃO PARA ABRIR MODAL DE EXCLUSÃO
function abrirModalExcluir(id, titulo) {
    console.log('Abrindo modal de exclusão para receita:', id);
    document.getElementById('delete_receita_id').value = id;
    document.getElementById('delete_receita_nome').textContent = titulo;
    
    // Atualizar action do formulário
    const deleteUrl = document.getElementById('formExcluirReceita').dataset.deleteUrl;
    document.getElementById('formExcluirReceita').action = deleteUrl.replace('0', id);
    
    // Abrir modal
    var modalElement = document.getElementById('modalExcluirReceita');
    var modal = new bootstrap.Modal(modalElement);
    modal.show();
}

// ALTERNAR ENTRE SEÇÕES (RECEITAS E UPLOAD)
function alternarSecao(secao) {
    const btnReceitas = document.getElementById('btnReceitas');
    const btnUpload = document.getElementById('btnUploadImagem');
    const secaoReceitas = document.getElementById('secaoReceitas');
    const secaoUpload = document.getElementById('secaoUpload');

    if (secao === 'receitas') {
        // Ativar botão Receitas
        btnReceitas.classList.add('active');
        btnUpload.classList.remove('active');
        
        // Mostrar seção Receitas
        secaoReceitas.style.display = 'block';
        secaoUpload.style.display = 'none';
    } else if (secao === 'upload') {
        // Ativar botão Upload
        btnUpload.classList.add('active');
        btnReceitas.classList.remove('active');
        
        // Mostrar seção Upload
        secaoUpload.style.display = 'block';
        secaoReceitas.style.display = 'none';
    }
}

// VARIÁVEL GLOBAL PARA ARMAZENAR O SLOT ATUAL
let slotAtual = null;

// ABRIR MODAL DE SELEÇÃO DE RECEITA
function abrirModalSelecaoReceita(event, slot) {
    event.preventDefault();
    slotAtual = slot;
    
    // Abrir modal
    const modalElement = document.getElementById('modalSelecionarReceita');
    const modal = new bootstrap.Modal(modalElement);
    modal.show();
}

// SELECIONAR RECEITA E ATUALIZAR CARD
function selecionarReceita(id, titulo, imagemUrl, descricao) {
    if (slotAtual === null) return;
    
    const card = document.querySelector(`.card-destaque[data-slot="${slotAtual}"]`);
    
    if (card) {
        // Atualizar conteúdo do card
        card.classList.remove('slot-destaque-vazio');
        card.classList.add('slot-destaque-preenchido');
        card.setAttribute('data-receita-id', id);
        
        card.innerHTML = `
            <div class="receita-selecionada-preview">
                <img src="${imagemUrl}" alt="${titulo}" class="receita-preview-img">
                <div class="receita-preview-info">
                    <h6 class="receita-preview-titulo">${titulo}</h6>
                    <p class="receita-preview-desc">${descricao.substring(0, 80)}...</p>
                </div>
                <button type="button" class="btn-remover-receita" onclick="removerReceitaDestaque(event, ${slotAtual})">
                    <i class="fa-solid fa-x"></i>
                </button>
            </div>
        `;
        
        // Atualizar preview do carrossel com a imagem da receita
        atualizarCarrosselPreview(slotAtual, imagemUrl, titulo, descricao);
    }
    
    // Fechar modal
    const modalElement = document.getElementById('modalSelecionarReceita');
    const modal = bootstrap.Modal.getInstance(modalElement);
    modal.hide();
}

// REMOVER RECEITA DO SLOT
function removerReceitaDestaque(event, slot) {
    event.preventDefault();
    event.stopPropagation();
    
    const card = document.querySelector(`.card-destaque[data-slot="${slot}"]`);
    if (card) {
        card.classList.remove('slot-destaque-preenchido');
        card.classList.add('slot-destaque-vazio');
        card.removeAttribute('data-receita-id');
        card.innerHTML = `
            <i class="fa-solid fa-circle-plus icone-destaque mb-3"></i>
            <p class="text-muted mb-0 fw-semibold">Adicionar Receita ${parseInt(slot) + 1}</p>
        `;
    }
    // Restaurar slide do carrossel correspondente
    if (typeof restaurarSlideCarrossel === 'function') {
        restaurarSlideCarrossel(Number(slot));
    }
}

// FILTRAR RECEITAS NA BUSCA
function filtrarReceitas() {
    const input = document.getElementById('buscarReceitaInput');
    const filtro = input.value.toLowerCase();
    const listaReceitas = document.getElementById('listaReceitas');
    const cards = listaReceitas.getElementsByClassName('card-receita-selecao');
    
    for (let i = 0; i < cards.length; i++) {
        const card = cards[i];
        const nomeReceita = card.querySelector('.receita-titulo').textContent.toLowerCase();
        
        if (nomeReceita.includes(filtro)) {
            card.parentElement.style.display = '';
        } else {
            card.parentElement.style.display = 'none';
        }
    }
}

// Função global para verificar se o slot do carrossel está preenchido (imagem ou receita)
function verificarSlotPreenchido(index) {
    const carouselItems = document.querySelectorAll('#carrosselPreview .carousel-item');
    if (!carouselItems[index]) return false;
    const slideContent = carouselItems[index].innerHTML;
    // Verifica se tem imagem de upload (carousel-slide-image) ou receita (carousel-slide-destaque)
    const temImagemUpload = slideContent.includes('carousel-slide-image');
    const temReceita = slideContent.includes('carousel-slide-destaque');
    return temImagemUpload || temReceita;
}

// INICIALIZAR EVENTOS AO CARREGAR A PÁGINA
document.addEventListener('DOMContentLoaded', function() {
    // Adicionar evento de click aos cards de destaque apenas para seleção de receita
    const cardsDestaque = document.querySelectorAll('.card-destaque');
    cardsDestaque.forEach(card => {
        card.addEventListener('click', function(e) {
            // Só bloquear se estiver na aba de receitas
            if (document.getElementById('secaoReceitas').style.display !== 'none') {
                const slot = this.getAttribute('data-slot');
                if (typeof verificarSlotPreenchido === 'function' && verificarSlotPreenchido(Number(slot))) {
                    const texto = document.getElementById('textoAvisoSlotPreenchido');
                    if (texto) {
                        texto.innerHTML = `O Slide ${Number(slot) + 1} já está preenchido!<br>Para adicionar uma nova receita ou imagem, remova o conteúdo atual clicando no botão X.`;
                    }
                    const modalAviso = new bootstrap.Modal(document.getElementById('modalAvisoSlotPreenchido'));
                    modalAviso.show();
                    e.preventDefault();
                    return;
                }
                abrirModalSelecaoReceita(e, slot);
            }
        });
    });
});
