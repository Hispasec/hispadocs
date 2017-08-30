from lxml import etree

from hispadocs.odt import OdtFile
from jinja2.environment import Environment

TEXT_NAMESPACE = 'urn:oasis:names:tc:opendocument:xmlns:text:1.0'

jinja_env = Environment()


def odt_template(path, variables):
    odt = OdtFile(path)
    tpl_body = odt.read_content()
    root = etree.fromstring(tpl_body)
    nodes = root.findall(".//{%s}*" % TEXT_NAMESPACE)
    for node in nodes:
        if node.text is None:
            continue
        node.text = jinja_env.from_string(node.text).render(**variables)
    out = etree.tostring(root)
    odt.write_content(out)

