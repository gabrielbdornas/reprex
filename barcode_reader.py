from pyzbar.pyzbar import decode
from pdf2image import convert_from_path
import os
from dotenv import load_dotenv
load_dotenv()

cemig_pwd = os.getenv('CEMIG_USER')

def barcode_reader(pdf_path, password=None):
  img = convert_from_path(pdf_path=pdf_path, dpi=300, userpw=password)[0]
  detected_barcodes = decode(img)
  if not detected_barcodes:
    return False
  else:
    for barcode in detected_barcodes: # poderia ter utilizado uma list comprehension aqui, mas preferi deixar mais explícito para facilitar o entendimento
    #   breakpoint()
      if barcode.data != '' and barcode.type == 'I25':
        return barcode.data.decode('utf-8')

if __name__ == "__main__":
    # Converte pdf para imagem, decodifica o código de barras e extrai a string do boleto
    cemig = os.listdir('pdfs')[0]
    cemig_img = convert_from_path(pdf_path=f'pdfs/{cemig}', dpi=300, userpw=cemig_pwd) # 300 do dpi é a resolução da imagem, ele usou 500
    cemig_img_decoded =decode(cemig_img[0])
    cemig_string = cemig_img_decoded[2].data.decode('utf-8')

    condominio = os.listdir('pdfs')[1]
    condominio_img = convert_from_path(pdf_path=f'pdfs/{condominio}', dpi=300, userpw='')
    condominio_img_decoded =decode(condominio_img[0])
    condominio_string = condominio_img_decoded[1].data.decode('utf-8')
    # condominio_img_decoded[1].type retornará I25 que é o tipo trabalhado para boleto.
    # I25 pode ser utilizado para certificar que estou tirando apenas códigos de boletos.
    # Poderia ser utilizado pix, mas pode gerar confusão com outros qr codes que não são pix.

    for bill in os.listdir('pdfs'):
        # breakpoint()
        pwd = cemig_pwd if bill == 'cemig.pdf' else None
        code = barcode_reader(f'pdfs/{bill}', password=pwd)
        print(f'{bill}: {code}')
