from fontTools.ttLib import TTFont

# https://github.com/fonttools/fonttools/tree/main/Snippets

WINDOWS_ENGLISH_IDS = 3, 1, 0x409
MAC_ROMAN_IDS = 1, 0, 0

FAMILY_RELATED_IDS = dict(
    LEGACY_FAMILY=1,
    TRUETYPE_UNIQUE_ID=3,
    FULL_NAME=4,
    POSTSCRIPT_NAME=6,
    PREFERRED_FAMILY=16,
    WWS_FAMILY=21,
)


def get_current_family_name(table):
    family_name_rec = None
    for plat_id, enc_id, lang_id in (WINDOWS_ENGLISH_IDS, MAC_ROMAN_IDS):
        for name_id in (
            FAMILY_RELATED_IDS["PREFERRED_FAMILY"],
            FAMILY_RELATED_IDS["LEGACY_FAMILY"],
        ):
            family_name_rec = table.getName(
                nameID=name_id,
                platformID=plat_id,
                platEncID=enc_id,
                langID=lang_id,
            )
            if family_name_rec is not None:
                break
        if family_name_rec is not None:
            break
    if not family_name_rec:
        raise ValueError("family name not found; can't add suffix")
    return family_name_rec.toUnicode()


def rename_family(font, repl_func, rehearsal=False):
    table = font["name"]
    family_name = get_current_family_name(table)
    for rec in table.names:
        name_id = rec.nameID
        if name_id not in FAMILY_RELATED_IDS.values():
            continue
        old_name = rec.toUnicode()
        new_name = repl_func(old_name)
        if rehearsal:
            rec.string = new_name
        print(f"[{rec}] {old_name} -> {new_name}")
    return family_name


def name_mapping(name):
    return name

font = TTFont("SFMono+SC-Regular.ttf")
family_name = rename_family(font, name_mapping, rehearsal=True)
# font.save("SFMono+SC-Regular.rename.ttf")

font = TTFont("SFMono+SC-Bold.ttf")
family_name = rename_family(font, name_mapping, rehearsal=True)
# font.save("SFMono+SC-Bold.rename.ttf")
