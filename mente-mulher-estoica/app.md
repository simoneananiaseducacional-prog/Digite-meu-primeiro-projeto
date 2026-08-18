# App Mente Mulher Estoica · Esboço

Planejamento inicial do app que vai vender conteúdos estoicos. Este documento é o
mapa: conceito, telas, versão mínima (MVP), ideias de tecnologia e próximos passos.

---

## Conceito em uma frase

Um app onde mulheres em reconstrução emocional encontram, todo dia, uma reflexão
estoica curta e podem aprofundar comprando ebooks, o diário guiado e cursos.

## Para quem

Mulheres de 25 a 45 anos, muitas mães, cansadas de sobreviver no impulso, na culpa
e na comparação. Buscam autocontrole, fé, valor próprio e elegância interior.

## Promessa

Sair do impulso e da culpa, um dia de cada vez, com filosofia prática e fé.

---

## Telas principais

1. **Início (Reflexão do dia)** — a frase estoica de hoje, com espaço para registro.
2. **Diário** — histórico de reflexões e anotações da usuária.
3. **Biblioteca** — ebooks, cursos e o diário guiado, à venda ou já adquiridos.
4. **Séries** — destaque para *Bíblia e Estoicismo*.
5. **Perfil e plano** — assinatura, compras e configurações.

## MVP (primeira versão, o mínimo que já entrega valor)

- [ ] Tela de Reflexão do dia (conteúdo estático rotativo).
- [ ] Registro simples no diário (salvo no aparelho).
- [ ] Vitrine de 1 diário digital + 1 ebook, com botão de compra.
- [ ] Plano gratuito (Semente) funcionando.

> Objetivo do MVP: provar que as mulheres voltam todo dia e que compram o primeiro produto.

## Depois do MVP

- Login e sincronização entre aparelhos.
- Pagamento recorrente (plano Raiz e Rocha).
- Cursos curtos em vídeo.
- Notificação diária da reflexão.

---

## Ideias de tecnologia

Nada definido ainda. Opções, do mais simples ao mais completo:

| Caminho | Bom para | Observação |
| --- | --- | --- |
| **Site/PWA** (HTML, CSS, JS) | Começar rápido e barato, funciona no celular como app | Ótimo para o MVP. Já dá para prototipar aqui no repositório. |
| **No-code** (ex.: Glide, Softr) | Publicar sem programar | Menos controle da estética. |
| **App nativo** (Flutter, React Native) | Experiência completa nas lojas | Mais trabalho, deixar para depois de validar. |

**Recomendação:** começar como **PWA** (um site que instala no celular). É o menor
esforço para validar, e o protótipo em `prototipo/index.html` já mostra o visual.

## Estética e voz (não negociáveis)

- Preto e branco editorial, preto e dourado, tipografia serifada, muito respiro.
- Voz direta, introspectiva, firme. Sem exclamação, sem travessão, sem clichê de coach.
- Fecho em imperativo universal.

---

## Próximos passos

1. Aprovar o catálogo de produtos (`produtos.md`).
2. Escolher o produto de estreia (sugestão: diário digital em PDF).
3. Evoluir o protótipo HTML para as telas do MVP.
4. Reunir o conteúdo das primeiras reflexões diárias (30 a 90 dias).
