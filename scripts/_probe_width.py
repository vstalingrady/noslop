import json
import pyarrow.parquet as pq
import pyarrow.compute as pc

tax = json.load(open(r"C:\Users\vstal\noslop\artifacts\taxonomy.json"))
fmap = {}
for k, v in tax["feature_taxonomy"].items():
    if not isinstance(v, dict) or "aspects" not in v:
        continue
    for asp in v["aspects"].values():
        for f in asp["features"]:
            fmap[f["id"]] = f

table = pq.read_table(
    r"C:\Users\vstal\noslop\third_party\storyscope\data\storyscope_features.parquet"
)


def uniques(col_name):
    col = table.column(col_name)
    u = pc.unique(col)
    return [x.as_py() for x in u if x.is_valid]


w_narr = 0
w_full = 0
for fid, f in fmap.items():
    sty = fid.startswith("STY_")
    t = f["type"]
    vals = uniques(fid)
    if t == "multi_select":
        atoms = set()
        for x in vals:
            if x is None or x == "":
                continue
            if isinstance(x, list):
                for p in x:
                    atoms.add(str(p))
            else:
                for p in str(x).split("|"):
                    p = p.strip()
                    if p:
                        atoms.add(p)
        n = len(atoms)
    elif t == "scale":
        n = 1
    else:
        atoms = set()
        for x in vals:
            if x is None:
                atoms.add("__MISSING__")
            else:
                atoms.add(str(x))
        n = len(atoms)
    w_full += n
    if not sty:
        w_narr += n
print("data-driven onehot (scale numeric) full", w_full, "narr", w_narr)

# variant: multi_select also +count
print(
    "plus ms count narr",
    w_narr + sum(1 for fid, f in fmap.items() if f["type"] == "multi_select" and not fid.startswith("STY_")),
)
