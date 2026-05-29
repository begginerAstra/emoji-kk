# Emoji KK — Demo de Identidade Visual para Discord

Este repositório prepara uma demo comercial para apresentar a ideia de **identidade visual usando emojis personalizados em servidores Discord**.

A ideia não é vender apenas emojis. A ideia é vender um pacote visual e funcional:

- emojis personalizados estáticos e animados;
- textos prontos para painéis;
- organização por função;
- painéis com aparência profissional;
- base para tickets, loja, staff, avisos, VIP, ranking e economia.

## Objetivo da demo

Quando aparecer um cliente, a apresentação já estará pronta para mostrar como o servidor dele pode ficar mais bonito, organizado e com identidade própria.

A demo mostra:

1. listagem dos emojis do servidor;
2. mapeamento dos emojis por função;
3. painel visual com botões;
4. textos prontos para copiar e adaptar;
5. roteiro de apresentação para vender a ideia.

## Comandos do bot

### Comandos de prefixo

```txt
!ajuda
!emojis
!mapear
!demo
```

### Slash commands

```txt
/demo
/emoji_lista
```

## Como apresentar para um cliente

1. Abra um servidor de teste no Discord.
2. Rode `!emojis` para mostrar que os emojis personalizados foram reconhecidos.
3. Rode `!mapear` para mostrar que os emojis podem ser separados por função.
4. Rode `/demo` ou `!demo` para mostrar o painel visual.
5. Explique que aquilo é uma base e pode virar um sistema completo.

## Frase principal da proposta

> Não é só um pacote de emojis. É uma identidade visual para o servidor, com painéis, textos, organização e sistemas prontos para deixar tudo mais profissional.

## Exemplos de uso

- `<:ticket:...>` para suporte e atendimento;
- `<:staff:...>` para painel da equipe;
- `<a:y_coin:...>` para sistema de moedas;
- `<:store:...>` para loja;
- `<:Check:...>` para aprovação;
- `<:X_:...>` para erro ou negação;
- `<a:loading:...>` para carregamento;
- `<a:fogo_azul:...>` para destaque visual.

## Como hospedar

Configure na hospedagem:

```txt
Start Command: python main.py
```

Variável de ambiente:

```txt
DISCORD_TOKEN=seu_token_do_bot
```

Dependência:

```txt
discord.py==2.4.0
```
