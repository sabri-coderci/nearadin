import os
import xml.etree.ElementTree as ET

def split_sitemap(input_file="sitemap.xml", output_dir="site-map", index_filename="sitemap-web.xml", domain="https://nearadin.net", limit=500):
    os.makedirs(output_dir, exist_ok=True)

    # Kaynak sitemap dosyasını oku
    tree = ET.parse(input_file)
    root = tree.getroot()

    # Namespace bağımsız tüm <url> etiketlerini topla
    raw_urls = [elem for elem in root.iter() if elem.tag.endswith('url')]

    if not raw_urls:
        print(f"{input_file} içinde hiçbir <url> etiketi bulunamadı!")
        return

    NS = "http://www.sitemap.org/schemas/sitemap/0.9"
    ET.register_namespace('', NS)

    # URL'leri 500'erli gruplara ayır
    chunks = [raw_urls[i:i + limit] for i in range(0, len(raw_urls), limit)]
    created_files = []

    # 1. Alt site haritalarını temiz namespace ile oluştur
    for index, chunk in enumerate(chunks, start=1):
        filename = f"sitemap-web-{index}.xml"
        filepath = os.path.join(output_dir, filename)
        created_files.append(filename)

        urlset = ET.Element(f"{{{NS}}}urlset")
        
        for raw_url in chunk:
            url_elem = ET.SubElement(urlset, f"{{{NS}}}url")
            for child in raw_url:
                tag_name = child.tag.split('}')[-1]  # Eski namespace'i temizle
                child_elem = ET.SubElement(url_elem, f"{{{NS}}}{tag_name}")
                child_elem.text = child.text

        out_tree = ET.ElementTree(urlset)
        ET.indent(out_tree, space="  ")
        out_tree.write(filepath, encoding="utf-8", xml_declaration=True)

    # 2. Ana sitemapindex dosyasını temiz namespace ile oluştur
    sitemapindex = ET.Element(f"{{{NS}}}sitemapindex")
    for file in created_files:
        sitemap_elem = ET.SubElement(sitemapindex, f"{{{NS}}}sitemap")
        loc = ET.SubElement(sitemap_elem, f"{{{NS}}}loc")
        loc.text = f"{domain}/{output_dir}/{file}"

    index_tree = ET.ElementTree(sitemapindex)
    ET.indent(index_tree, space="  ")
    index_filepath = os.path.join(output_dir, index_filename)
    index_tree.write(index_filepath, encoding="utf-8", xml_declaration=True)

    print("İşlem başarıyla tamamlandı. Ad alanları Google standartlarına göre temizlendi.")

if __name__ == "__main__":
    split_sitemap()
