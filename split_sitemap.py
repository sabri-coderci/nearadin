import xml.etree.ElementTree as ET

def split_sitemap(input_file="sitemap.xml", domain="https://nearadin.net", limit=500):
    # XML dosyasını ayrıştır
    tree = ET.parse(input_file)
    root = tree.getroot()

    # Namespace fark etmeksizin tüm <url> etiketlerini yakala
    urls = [elem for elem in root.iter() if elem.tag.endswith('url')]

    if not urls:
        print("Sitemap içinde hiçbir <url> etiketi bulunamadı!")
        return

    # URL'leri 500'erli parçalara böl
    chunks = [urls[i:i + limit] for i in range(0, len(urls), limit)]
    created_files = []

    ns_uri = "http://www.sitemap.org/schemas/sitemap/0.9"
    ET.register_namespace('', ns_uri)

    for index, chunk in enumerate(chunks, start=1):
        filename = f"sitemap-{index}.xml"
        created_files.append(filename)

        urlset = ET.Element(f"{{{ns_uri}}}urlset")
        for url in chunk:
            urlset.append(url)

        out_tree = ET.ElementTree(urlset)
        ET.indent(out_tree, space="  ")
        out_tree.write(filename, encoding="utf-8", xml_declaration=True)

    # Index dosyasını oluştur
    sitemapindex = ET.Element(f"{{{ns_uri}}}sitemapindex")
    for file in created_files:
        sitemap_elem = ET.SubElement(sitemapindex, f"{{{ns_uri}}}sitemap")
        loc = ET.SubElement(sitemap_elem, f"{{{ns_uri}}}loc")
        loc.text = f"{domain}/{file}"

    index_tree = ET.ElementTree(sitemapindex)
    ET.indent(index_tree, space="  ")
    index_tree.write("sitemap_index.xml", encoding="utf-8", xml_declaration=True)

if __name__ == "__main__":
    split_sitemap(input_file="sitemap.xml", domain="https://nearadin.net")
