import xml.etree.ElementTree as ET

def split_sitemap(input_file="sitemap_big.xml", domain="https://siteadi.com", limit=500):
    # XML namespace tanımları
    ns = {'ns': 'http://www.sitemap.org/schemas/sitemap/0.9'}
    ET.register_namespace('', ns['ns'])

    tree = ET.parse(input_file)
    root = tree.getroot()
    urls = root.findall('ns:url', ns)

    # URL'leri 500'erli parçalara ayır
    chunks = [urls[i:i + limit] for i in range(0, len(urls), limit)]
    created_files = []

    for index, chunk in enumerate(chunks, start=1):
        filename = f"sitemap-{index}.xml"
        created_files.append(filename)

        urlset = ET.Element("urlset", xmlns=ns['ns'])
        for url in chunk:
            urlset.append(url)

        out_tree = ET.ElementTree(urlset)
        ET.indent(out_tree, space="  ")
        out_tree.write(filename, encoding="utf-8", xml_declaration=True)

    # Sitemap Index dosyasını oluştur
    sitemapindex = ET.Element("sitemapindex", xmlns=ns['ns'])
    for file in created_files:
        sitemap_elem = ET.SubElement(sitemapindex, "sitemap")
        loc = ET.SubElement(sitemap_elem, "loc")
        loc.text = f"{domain}/{file}"

    index_tree = ET.ElementTree(sitemapindex)
    ET.indent(index_tree, space="  ")
    index_tree.write("sitemap_index.xml", encoding="utf-8", xml_declaration=True)

if __name__ == "__main__":
    split_sitemap()
