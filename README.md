# Projeto JobScraper - Centralize as Vagas Online

O JobScraper é usado puramente para recolher vagas de empregos nos domínios
especificados abaixo, os centralizando em um arquivo .xlsx:

* LinkedIn
* Vagas.com

## Instalação

Use o gerenciador de pacotes ['pip'](https://pypi.org/project/pip/) para
instalar o JobScraper:

```bash
pip install JobScraper
```

## Utilização

```python
import JobScraper

# Coloque suas pesquisas em uma lista.
query_list = [
    "query 1",
    "query 2",
    "query 3",
    "query n",
]

# Crie o objeto com a classe JobScraper.
objeto = JobScraper(
    dominio="palavra-chave",  # Consulte as palavras-chave
    archive_name="sua-escolha",
    query=query_list,
)

# Instancie o objeto com a seguinte função.
objeto.criar_arquivo()
```

A execução deste código irá ativar o Selenium, recolher os dados das vagas
e armazená-los em um arquivo .xlsx, que por ventura será criado no mesmo local
onde está localizado o módulo de execução deste pacote.

### Sobre o arquivo .xlsx

Como anteriormente dito, o arquivo será criado no diretório do módulo de
execução, o nome deste será decidido no momento de criação do objeto. Em casos
de arquivos com o mesmo nome, este será simplesmente atualizado.

Arquivos .xlsx possuem planilhas, estas são nomeadas de acordo com a palavra-
chave utilizada no parâmetro "dominio", na criação do objeto. Em situações onde
o usuário utilize o mesmo nome de arquivo em uma pesquisa nova, em adição a
isso, o mesmo nome de planilha, todos os dados da planilha antiga serão
**apagados** e novos dados serão postos no lugar, fique ciente disso.

Em casos de arquivos com o mesmo nome, porém planilhas com nomes diferentes,
uma nova planilha será adicionada ao arquivo já existente.

### Palavras-chave

* "linkedin"
---> Domínio Utilizado: [LinkedIn](https://www.linkedin.com/jobs/)
---> Nome da Planilha: "linkedin"

* "vagas.com"
---> Domínio Utilizado: [Vagas.com](https://www.vagas.com.br/)
---> Nome da Planilha: "vagas.com"

## Desenvolvedor

Lucas Aquino de Oliveira
---> [Meu LinkedIn](https://www.linkedin.com/in/aquino-lucas)