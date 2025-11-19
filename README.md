# 🍽️ Cozinha Inclusiva

<p align="center">
  <em>Portal de receitas adaptadas para dietas restritivas, focado em sabor, bem-estar e inclusão alimentar.✨💚</em> 
</p>

---

## 📖 Sobre o Projeto

O **Cozinha Inclusiva** é um projeto de desenvolvimento web focado em criar um site de receitas completo e acessível, pensado especificamente para pessoas com **restrições alimentares** — como intolerância à lactose, glúten, carne (dietas veganas/vegetarianas) ou outras necessidades dietéticas.

A missão é reunir receitas **criativas e saborosas**, desde as mais simples até as mais elaboradas, garantindo que o foco esteja sempre no sabor e no respeito às diferentes escolhas e restrições. A plataforma busca criar um ambiente visualmente acolhedor e informativo para todos os usuários.

---

### Público-Alvo

* Pessoas com **intolerâncias alimentares** (lactose, glúten, etc.).
* Indivíduos em **dietas restritivas** (veganas, dietéticas, etc.).
* Qualquer pessoa interessada em explorar uma **alimentação mais consciente** e saudável.

---

## ✨ Funcionalidades

O sistema é dividido em duas grandes áreas: o **Site Público** para visitantes e o **Painel Administrativo** para gerenciamento de conteúdo, atendendo a perfis de acesso específicos.

- 🥗 **Navegação e Conteúdo Público:**
    - Página inicial com destaques e página de **categorias** (`Sem Lactose`,`Sem Glúten`, `Veganas`, `Dietéticas`).
    - **Sistema de busca** eficiente por ingredientes e restrições alimentares.
    - Página de receita detalhada e área de **comentários** para interação.

- ⚙️ **Gerenciamento Administrativo (Backend):**
    - **Login restrito** e **Dashboard** interativo para análise de dados.
    - **CRUD (Criação, Leitura, Atualização, Exclusão)** completo de Receitas e Categorias.
    - **CRUD de Comentários** para moderação e gestão de interações.

- 👥 **Papéis e Perfis de Usuários:**

   O sistema Cozinha Inclusiva possui três perfis de usuários com diferentes níveis de acesso e responsabilidade:
  
    - **Gerente (Chef):** Acessa o gerenciamento de receitas, categorias, comentários e o Dashboard.
    - **Administrador (Desenvolvedor):** Acesso total para suporte e manutenção do sistema.
    - **Usuários Comuns (Visitantes):** Navega no site, comenta e compartilha.

---

## 🛠️ Tecnologias Utilizadas

O projeto utiliza a stack **Python/Django**, reconhecida por sua robustez e eficiência em desenvolvimento web de larga escala.

- **Backend:** **Python** (Linguagem de Programação principal).
- **Framework Web:** **Django** (Framework de alto nível para desenvolvimento rápido e seguro).
- **Frontend:** HTML5, CSS3, JavaScript.
- **Banco de Dados:** Modelo Relacional (SQL) compatível com o Django ORM.

---

## 📄 Estrutura de Aplicações e BD

O projeto utiliza um **modelo de dados relacional** focado na organização eficiente de receitas, ingredientes e interações do usuário.

### Entidades Principais

| Entidade | Atributos Principais |
| :--- | :--- |
| **USUARIO** | ID\_USUARIO (PK), NOME, EMAIL, SENHA, TIPO, IMAGEM |
| **CATEGORIA** | ID\_CATEGORIA (PK), NOME, VIZUALIZACAO\_TOTAL, RECEITA\_POPULAR, DATA\_CRIACAO |
| **RECEITA** | ID\_RECEITA (PK), NOME, DESCRICAO, DATA\_PUBLICACAO, VIZUALIZACOES, IMAGEM\_CAPA |
| **INGREDIENTE** | ID\_INGREDIENTE (PK), NOME |

### Entidades de Apoio e Relacionamento

| Entidade | Relacionamento Principal | Tabela de Ligação |
| :--- | :--- | :--- |
| **MODO\_PREPARO** | **RECEITA** (1:N) | N/A |
| **COMENTARIO** | **RECEITA** (N:1), **USUARIO** (N:1) | N/A |
| **CATEGORIA** / **RECEITA** | N:N | **CATEGORIA\_RECEITA** |
| **INGREDIENTE** / **RECEITA** | N:N | **RECEITA\_INGREDIENTE** |

---

## 🎨 Estilo Visual e Design

A identidade visual foi cuidadosamente planejada para ser acolhedora (**afetiva**) e confiável (**clara**), essencial para acolher o publico-alvo.

### **🖋️ Tipografia**

| Fonte | Uso Principal | Sensação Transmitida |
| :--- | :--- | :--- |
| **Dancing Script** | Títulos de Receitas e Cabeçalhos. | Afetivo, humanizado e divertido. |
| **Open Sans** | Textos Corridos, Instruções e Listas. | Confiável, leve e clara. |

**Import Google Fonts:**
```html
<link href="[https://fonts.googleapis.com/css2?family=Dancing+Script:wght@400..700&family=Open+Sans:ital,wght@0,300..800;1,300..800&display=swap](https://fonts.googleapis.com/css2?family=Dancing+Script:wght@400..700&family=Open+Sans:ital,wght@0,300..800;1,300..800&display=swap)" rel="stylesheet">
```

### **🌈 Paleta de Cores**

| Cor | Hex Code | Uso Principal e Significado |
| :--- | :--- | :--- | 
| **Verde Claro** | `#b4d39d` | *Cor Principal* Associado à saúde, vitalidade, equilíbrio e tranquilidade. Reforça a ideia de alimentação consciente e segura. |
| **Marrom Escuro** | `#5d3c2a` | Estabilidade e segurança, evocando conforto e aconchego em elementos do site. |
| **Marrom Avermelhado** | `#985942` | Associado à terra e confiabilidade. Eficaz para estimular o apetite em conteúdos relacionados à comida. |
| **Bege Claro** | `#f0d3bc` | Neutralidade e suavidade. Ideal para fundos ou áreas de descanso visual. |

## 🚀 Próximos Passos e Complementos Futuros

O projeto prevê expansões futuras para aprimorar a experiência do usuário e a gestão de conteúdo, incluindo:

- 🖼️ Carrossel de Destaques (**CARROSSEL_DESTAQUE**).
- 📄 Gerenciamento de Conteúdo Estático do site (**CONTEUDO_SITE**).
- 🛡️ Sistema de Moderação de Comentários (**MODERACAO e COMENTARIO_MODERADO**).
