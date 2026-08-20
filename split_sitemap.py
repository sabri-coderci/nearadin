import os
import xml.etree.ElementTree as ET

def split_sitemap(input_file="sitemap.xml", output_dir="site-map", index_filename="sitemap-web.xml", domain="https://nearadin.net", limit=500):
    # Klasör yoksa otomatik oluştur
    os.makedirs(output_dir, exist_ok=True)

    # Kaynak sitemap dosyasını oku
    tree = ET.parse(input_file)
    root = tree.getroot()

    # Namespace bağımsız tüm <url> etiketlerini topla
    urls = [elem for elem in root.iter() if elem.tag.endswith('url')]

    if not urls:
        print(f"{input_file} içinde hiçbir <url> etiketi bulunamadı!")
        return

    ns_uri = "http://www.sitemap.org/schemas/sitemap/0.9"
    ET.register_namespace('', ns_uri)

    # URL'leri 500'erli gruplara ayır
    chunks = [urls[i:i + limit] for i in range(0, len(urls), limit)]
    created_files = []

    # 1. Alt site haritalarını site-map/ klasörüne kaydet
    for index, chunk in enumerate(chunks, start=1):
        filename = f"sitemap-web-{index}.xml"
        filepath = os.path.join(output_dir, filename)
        created_files.append(filename)

        urlset = ET.Element(f"{{{ns_uri}}}urlset")
        for url in chunk:
            urlset.append(url)

        out_tree = ET.ElementTree(urlset)
        ET.indent(out_tree, space="  ")
        out_tree.write(filepath, encoding="utf-8", xml_declaration=True)

    # 2. Ana dizin dosyasını site-map/sitemap-web.xml olarak kaydet
    sitemapindex = ET.Element(f"{{{ns_uri}}}sitemapindex")
    for file in created_files:
        sitemap_elem = ET.SubElement(sitemapindex, f"{{{ns_uri}}}sitemap")
        loc = ET.SubElement(sitemap_elem, f"{{{ns_uri}}}loc")
        # URL yapısını klasör adına göre günceller
        loc.text = f"{domain}/{output_dir}/{file}"

    index_tree = ET.ElementTree(sitemapindex)
    ET.indent(index_tree, space="  ")
    index_filepath = os.path.join(output_dir, index_filename)
    index_tree.write(index_filepath, encoding="utf-8", xml_declaration=True)
    
    print(f"Başarılı: '{output_dir}/' klasörüne '{index_filename}' ve alt dosyalar yazıldı.")

if __name__ == "__main__":
    split_sitemap(
        input_file="sitemap.xml", 
        output_dir="site-map", 
        index_filename="sitemap-web.xml", 
        domain="https://nearadin.net"
    )
