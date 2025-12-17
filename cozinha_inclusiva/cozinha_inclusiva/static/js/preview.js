// JAVASCRIPT PARA PRÉ-VISUALIZAÇÃO DE IMAGENS NO UPLOAD E CARROSSEL

// PREVIEW DA IMAGEM CARREGADA
function previewImage(input, index) {
    // Bloqueio global: se o carrossel já está preenchido, não permite upload
    if (typeof verificarSlotPreenchido === 'function' && verificarSlotPreenchido(index)) {
        const texto = document.getElementById('textoAvisoSlotPreenchido');
        if (texto) {
            texto.innerHTML = `O Slide ${index + 1} já está preenchido!<br>Para adicionar uma nova imagem ou receita, remova o conteúdo atual clicando no botão X.`;
        }
        const modalAviso = new bootstrap.Modal(document.getElementById('modalAvisoSlotPreenchido'));
        modalAviso.show();
        input.value = '';
        return;
    }

    const uploadContent = document.getElementById('uploadContent' + (index + 1));
    const previewContainer = document.getElementById('previewContainer' + (index + 1));
    const previewImg = document.getElementById('previewImg' + (index + 1));

    if (input.files && input.files[0]) {
        const reader = new FileReader();
        
        reader.onload = function(e) {
            previewImg.src = e.target.result;
            uploadContent.style.display = 'none';
            previewContainer.style.display = 'block';
            
            // Atualizar pré-visualização do carrossel
            atualizarCarrosselPreview(index, e.target.result);
        };
        
        reader.readAsDataURL(input.files[0]);
    }
}

// REMOVER IMAGEM
function removerImagem(index) {
    const uploadInput = document.getElementById('uploadInput' + (index + 1));
    const uploadContent = document.getElementById('uploadContent' + (index + 1));
    const previewContainer = document.getElementById('previewContainer' + (index + 1));
    const previewImg = document.getElementById('previewImg' + (index + 1));

    // Limpar input
    uploadInput.value = '';
    
    // Mostrar novamente o upload content
    uploadContent.style.display = 'block';
    previewContainer.style.display = 'none';
    previewImg.src = '';
    
    // Restaurar slide do carrossel
    restaurarSlideCarrossel(index);
}

// DETECTAR BRILHO DA IMAGEM
function detectarBrilhoImagem(imageSrc, callback) {
    const img = new Image();
    img.crossOrigin = 'Anonymous';
    
    // Tratamento de erro ao carregar a imagem
    img.onerror = function() {
        console.warn('Erro ao carregar imagem para análise de brilho. Usando valor padrão (escuro).');
        callback(false); // Assume fundo escuro em caso de erro
    };
    
    img.onload = function() {
        try {
            const canvas = document.createElement('canvas');
            const ctx = canvas.getContext('2d');
            
            // Redimensionar canvas para otimização (máx 200x200 para análise)
            const maxSize = 200;
            const scale = Math.min(maxSize / img.width, maxSize / img.height, 1);
            canvas.width = img.width * scale;
            canvas.height = img.height * scale;
            
            ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
            
            const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
            const data = imageData.data;
            
            // Verificar se é PNG com transparência
            const isPNG = imageSrc.toLowerCase().includes('data:image/png') || 
                        imageSrc.toLowerCase().endsWith('.png');
            
            if (isPNG) {
                let pixelsTransparentes = 0;
                let pixelsTotais = data.length / 4;
                
                // Contar pixels totalmente transparentes
                for (let i = 3; i < data.length; i += 4) {
                    if (data[i] === 0) {
                        pixelsTransparentes++;
                    }
                }
                
                // Se mais de 50% da imagem é transparente, usar texto escuro
                if (pixelsTransparentes > pixelsTotais * 0.5) {
                    callback(true); // true = usar texto escuro
                    return;
                }
            }
            
            // Calcular brilho médio dos pixels visíveis
            let brilhoTotal = 0;
            let pixelsContados = 0;
            const step = 4; // Amostragem: processar 1 a cada 4 pixels para otimização
            
            for (let i = 0; i < data.length; i += (step * 4)) {
                const alpha = data[i + 3];
                
                // Só considerar pixels visíveis (alpha > 128)
                if (alpha > 128) {
                    const r = data[i];
                    const g = data[i + 1];
                    const b = data[i + 2];
                    
                    // Fórmula de luminância percebida (padrão ITU-R BT.601)
                    const luminancia = (0.299 * r + 0.587 * g + 0.114 * b);
                    brilhoTotal += luminancia;
                    pixelsContados++;
                }
            }
            
            // Proteção contra divisão por zero
            if (pixelsContados === 0) {
                console.warn('Nenhum pixel visível encontrado. Usando valor padrão (escuro).');
                callback(false);
                return;
            }
            
            const brilhoMedio = brilhoTotal / pixelsContados;
            
            // Limiar ajustado: 128 é o ponto médio (0-255)
            // Imagens com brilho > 128 são consideradas claras
            const imagemClara = brilhoMedio > 128;
            
            // Debug: log do brilho calculado
            console.log(`Brilho médio da imagem: ${brilhoMedio.toFixed(2)} (${imagemClara ? 'CLARA' : 'ESCURA'})`);
            
            callback(imagemClara);
            
        } catch (erro) {
            console.error('Erro ao processar imagem:', erro);
            callback(false); // Assume fundo escuro em caso de erro
        }
    };
    
    img.src = imageSrc;
}

// ATUALIZAR CARROSSEL DE PRÉ-VISUALIZAÇÃO
function atualizarCarrosselPreview(index, imageSrc, titulo = null, descricao = null) {
    const textos = [
        'Receitas que acolhem todos os sabores',
        'Sabor e saúde em cada receita',
        'Cozinha inclusiva para todos'
    ];
    
    // Imagens de fundo para cada slide
    const fundos = [
        '/static/image/destaque/fundo-1.png',
        '/static/image/destaque/fundo-2.png',
        '/static/image/destaque/fundo-3.png'
    ];
    
    // Se foi passado título, usar ele ao invés do texto padrão
    const textoSlide = titulo || textos[index];
    
    const carouselItems = document.querySelectorAll('#carrosselPreview .carousel-item');
    if (carouselItems[index]) {
        // Se tem título (receita selecionada), usa layout especial com fundo
        if (titulo) {
            carouselItems[index].classList.remove('light-background', 'dark-background');
            carouselItems[index].innerHTML = `
                <div class="carousel-slide-destaque">
                    <img src="${fundos[index]}" alt="Background" class="slide-background">
                    <div class="slide-content-wrapper">
                        <img src="${imageSrc}" alt="${titulo}" class="receita-destaque-img">
                        <div class="receita-destaque-info">
                            <h2 class="receita-destaque-titulo">${titulo}</h2>
                            <button class="btn-ver-receita">Ver Receita</button>
                        </div>
                    </div>
                </div>
            `;
        } else {
            // Se não tem título (upload de imagem), usa layout original
            detectarBrilhoImagem(imageSrc, function(imagemClara) {
                const corTexto = imagemClara ? 'text-dark' : 'text-light';
                const classSlide = imagemClara ? 'light-background' : 'dark-background';
                
                carouselItems[index].classList.remove('light-background', 'dark-background');
                carouselItems[index].classList.add(classSlide);
                
                carouselItems[index].innerHTML = `
                    <div class="carousel-slide-image">
                        <img src="${imageSrc}" alt="Preview Slide ${index + 1}" style="width: 100%; height: 100%; object-fit: cover;">
                        <div class="carousel-slide-text ${corTexto}">
                            ${textoSlide}
                        </div>
                    </div>
                `;
            
                // Atualizar cor dos botões junto com o texto
                const carouselElement = document.getElementById('carrosselPreview');
                if (carouselElement) {
                    const prevIcon = carouselElement.querySelector('.carousel-control-prev-icon');
                    const nextIcon = carouselElement.querySelector('.carousel-control-next-icon');
                    
                    if (prevIcon && nextIcon) {
                        if (imagemClara) {
                            // Fundo claro - botões escuros
                            prevIcon.style.setProperty('filter', 'brightness(0) drop-shadow(0 0 2px rgba(0, 0, 0, 0.8))', 'important');
                            nextIcon.style.setProperty('filter', 'brightness(0) drop-shadow(0 0 2px rgba(0, 0, 0, 0.8))', 'important');
                        } else {
                            // Fundo escuro - botões brancos
                            prevIcon.style.setProperty('filter', 'brightness(0) invert(1) drop-shadow(0 0 2px rgba(255, 255, 255, 0.8))', 'important');
                            nextIcon.style.setProperty('filter', 'brightness(0) invert(1) drop-shadow(0 0 2px rgba(255, 255, 255, 0.8))', 'important');
                        }
                    }
                }
            });
        }
    }
}

// RESTAURAR SLIDE DO CARROSSEL
function restaurarSlideCarrossel(index) {
    const carouselItems = document.querySelectorAll('#carrosselPreview .carousel-item');
    if (carouselItems[index]) {
        carouselItems[index].classList.remove('light-background', 'dark-background');
        carouselItems[index].innerHTML = `
            <div class="carousel-slide-placeholder">
                <span class="text-muted fw-semibold">Slide ${index + 1} do Carrossel</span>
            </div>
        `;
        
        // Restaurar botões para branco (padrão)
        const carouselElement = document.getElementById('carrosselPreview');
        if (carouselElement) {
            const prevIcon = carouselElement.querySelector('.carousel-control-prev-icon');
            const nextIcon = carouselElement.querySelector('.carousel-control-next-icon');
            
            if (prevIcon && nextIcon) {
                prevIcon.style.setProperty('filter', 'brightness(0) invert(1) drop-shadow(0 0 2px rgba(255, 255, 255, 0.8))', 'important');
                nextIcon.style.setProperty('filter', 'brightness(0) invert(1) drop-shadow(0 0 2px rgba(255, 255, 255, 0.8))', 'important');
            }
        }
    }
}

// ATUALIZAR COR DOS BOTÕES QUANDO O SLIDE MUDAR (NAVEGAÇÃO)
document.addEventListener('DOMContentLoaded', function() {
    const carouselElement = document.getElementById('carrosselPreview');
    if (carouselElement) {
        // Atualizar cor dos botões quando o slide mudar
        carouselElement.addEventListener('slid.bs.carousel', function() {
            const activeSlide = carouselElement.querySelector('.carousel-inner .carousel-item.active');
            const prevIcon = carouselElement.querySelector('.carousel-control-prev-icon');
            const nextIcon = carouselElement.querySelector('.carousel-control-next-icon');
            
            if (activeSlide && prevIcon && nextIcon) {
                const hasLightBackground = activeSlide.outerHTML.includes('light-background');
                
                if (hasLightBackground) {
                    // Fundo claro - botões escuros
                    prevIcon.style.setProperty('filter', 'brightness(0) drop-shadow(0 0 2px rgba(0, 0, 0, 0.8))', 'important');
                    nextIcon.style.setProperty('filter', 'brightness(0) drop-shadow(0 0 2px rgba(0, 0, 0, 0.8))', 'important');
                } else {
                    // Fundo escuro - botões brancos
                    prevIcon.style.setProperty('filter', 'brightness(0) invert(1) drop-shadow(0 0 2px rgba(255, 255, 255, 0.8))', 'important');
                    nextIcon.style.setProperty('filter', 'brightness(0) invert(1) drop-shadow(0 0 2px rgba(255, 255, 255, 0.8))', 'important');
                }
            }
        });
    }
});
