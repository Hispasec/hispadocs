from ooopy.Transformer import Transformer
import ooopy.Transforms as Transforms
from ooopy.OOoPy import OOoPy


class OdtFiles(list):
    def __init__(self, files):
        super(OdtFiles, self).__init__(files)

    def create_output(self, output_path):
        o = OOoPy(infile=self[0], outfile=output_path)
        if len(self) > 1:
            t = Transformer(
                o.mimetype,
                Transforms.get_meta(o.mimetype),
                Transforms.Concatenate(*(self[1:])),
                Transforms.renumber_all(o.mimetype),
                Transforms.set_meta(o.mimetype),
                Transforms.Fix_OOo_Tag(),
                Transforms.Manifest_Append()
            )
            t.transform(o)
        o.close()
