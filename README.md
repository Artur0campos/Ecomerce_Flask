# 🚀 Project Name

<div align="left">
  <img alt="Python" src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img alt="Flask" src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white" />
  <img alt="SQLite" src="https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white" />
</div>

---

### 📝 Sobre o Projeto
Este projeto foi desenvolvido durante um minicurso prático da **Rocketseat**, focado em fundamentos de Backend com Python. A aplicação tem como objetivo principal [descreva aqui o objetivo, ex: gerenciar uma lista de tarefas ou contatos] de forma simples e eficiente.

> 🎓 **Certificado de Conclusão:** [Visualizar Certificado da Rocketseat](https://app.rocketseat.com.br/certificates/4c6a8ea4-af9b-4c1f-8d97-9f199ce0480d)

---

### 🏗️ Diferencial: Arquitetura MVC
Embora o projeto original seguisse uma estrutura linear, apliquei uma refatoração completa para o padrão **MVC (Model-View-Controller)**. 

Essa foi a única mudança estrutural feita em relação ao curso, com o objetivo de:
* **Model:** Isolar a lógica de dados e interação com o SQLite.
* **View:** Gerenciar a interface e o retorno ao usuário.
* **Controller:** Mediar a entrada de dados e a lógica de negócio.
* *Resultado:* Um código muito mais organizado, testável e fácil de dar manutenção.

---

### 📖 Documentação das Rotas

| Método | Rota | Descrição |
|:---:|:---:|:--- |
| `GET` | `/` | Retorna a página principal ou o status da aplicação. |
| `GET` | `/api/items` | Lista todos os registros armazenados no banco. |
| `POST` | `/api/items` | Cria um novo registro (requer JSON no corpo). |
| `PUT` | `/api/items/<id>` | Atualiza os dados de um registro específico. |
| `DELETE` | `/api/items/<id>` | Remove um registro do sistema permanentemente. |

---

### 🚀 Como executar
1. Clone o repositório:
   ```bash
   git clone [https://github.com/arturcampos100/nome-do-projeto.git](https://github.com/arturcampos100/nome-do-projeto.git)