from playwright.sync_api import sync_playwright


def main() -> None:
    cpf = input("Digite o cpf: ")
    passwd = input("\nDigite a pass: ")

    with sync_playwright() as playwright:
        browser = playwright.firefox.launch(headless=False)
        page = browser.new_page()
        page.goto("https://login.anhanguera.com/", wait_until="domcontentloaded")

        page.get_by_label("CPF").fill(cpf)
        page.get_by_role("button", name="Avançar").click()

        page.get_by_label("Senha").fill(passwd)
        page.get_by_role("button", name="Entrar").click()

        page.get_by_test_id("skip-mfa").click()
        
        page.locator("#meu_curso").click()
        page.get_by_role("presentation", name="Disciplina e notas").click()

        quadro_materias = page.locator("[ng-if=options.titulo]").all()
        nome_materias = [el.inner_text() for el in quadro_materias]

        page.get_by_role("presentation", name="Estudar").click()
        quadro_materias = page.locator("[ng-if=options.titulo]").all()
        nome_materias = [el.inner_text() for el in quadro_materias]

        page.get_by_role("presentation", name="Estudar").click()

        quadros_de_conteudo_AVA = page.locator(".card-content-title").all()
        nome_quadros_AVA = [el.inner_text() for el in quadros_de_conteudo_AVA]

        # Store matching materias
        materias_encontradas = [
            materia for materia in nome_materias if materia in nome_quadros_AVA
        ]

        # Show menu and ask user to pick
        if materias_encontradas:
            print("\nQual materia você quer fazer?")
            for i, materia in enumerate(materias_encontradas, start=1):
                print(f"{i}. {materia}")

            escolha = int(input("\nDigite o número da materia: "))
            materia_escolhida = materias_encontradas[escolha - 1]
            print(f"\nVocê escolheu: {materia_escolhida}")

            page.locator(".card-wrap").filter(has_text=materia_escolhida).locator(
                "button", has_text="Acessar a Disciplina"
            ).click()
        else:
            print("Nenhuma materia encontrada.")


if __name__ == "__main__":
    main()
