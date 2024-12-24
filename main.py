from app.core.website_content import Content

def main():
  autra = Content("https://www.astria.ai/p/stylish-studio-portraits")
  print(autra.get_images())

if __name__ == "__main__":
  main()