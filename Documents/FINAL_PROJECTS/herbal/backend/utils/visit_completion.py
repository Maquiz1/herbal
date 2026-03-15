# nimregenin/utils/visit_completion.py

def visit_crf_status(visit):

    crfs = {
        "crf1": hasattr(visit, "crf1"),
        "crf2": hasattr(visit, "crf2"),
        "crf3": hasattr(visit, "crf3"),
        "crf4": hasattr(visit, "crf4"),
        "crf7": hasattr(visit, "crf7"),
    }

    complete = all(crfs.values())

    return crfs, complete
