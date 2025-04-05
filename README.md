# Planejamento Projeto - Scraping de Vagas (Em andamento)

## Módulo 1 - Classe

**Scraping com Selenium (scraping):**

* init (domain, archive_name, query)
* Seleção do Dominio
* Método do Linkedin
* Método do Vagas.com
* Catho (?)
* Glassdoor (?)
* Programathor (?)
* Método de Criação
-----> Chamar a função de conversão
-----> Colocar os argumentos

* Implementar mensagens de sucesso --------------------------------- (X)
* Achar alguma forma de contornar as buscas sem resultado ---------- (X)
* Remover vagas duplicadas da lista aninhada ----------------------- (FEITO)
* Por favor, colabora comigo, chromewebdriver ---------------------- (FEITO)
* Resolver as chamadas de erro do log (incompatibilidade?) --------- (X)

## Módulo 2 - Função

**Transformar lista aninhada em XLSX (conversion):**

* Parâmetros (job_list, archive_name, sheet_name)
* Criar arquivo .xlsx
* Modificar arquivo se já criado

* Apagar planilha antiga se nova tem o mesmo nome ------------------ (FEITO)
* Resolver o sanhaço da planilha fantasma -------------------------- (FEITO)

## Usar JobScraper

* Criar uma lista de queries para a pesquisa (list[[str]]) - Lista Aninhada
* Instanciar o JobScraper
-----> Inserir domínio ("linkedin" ou "vagas.com")
-----> Inserir nome do arquivo (str)
-----> Inserir query (lista de queries vai aqui)

* Chamar o método de criação (objeto.criar_arquivo())