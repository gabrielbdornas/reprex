# Ler boletos de e-mail

- Vídeo YouTube: https://www.youtube.com/watch?v=MGQbY1PklCw&t=2735s
- Ler emails.
- Processar anexos.
- Anexos com códigos de barra as informações do boleto serão lidos.
- Lib python [imbox](https://pypi.org/project/imbox/) usando o gmail (por ser o mais geral).
- Lib python [pyzbar](https://pypi.org/project/pyzbar/).
- Lib python pdf2image.
- Lib pillow para automatização de imagem.
- Necessário instalar para pyzbar funcionar

```
sudo apt update
sudo apt install libzbar0
```

- trabalhar com imagem é melhor do que pdf. pdf é zoado
- minuto 44:01 ele mostra algumas referências para o que significam os números dos boletos.
- Achei este site https://www.boletobancario-codigodebarras.com/formulario-conversor/ que faz a conversão do código de barra para as informações de pagamento.
- Não achei uma lib python que faça a conversão da linha digitável para o qr code (poderia criar um meu).
 
