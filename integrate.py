

def parse_args(string):
    """
    Parameters

    string: this is a colon-separated string, the first field is the metric's unique name
        every other field is optional and is formatted as `key=value`.

    Return the metric name and a dictionary with (key, value) pairs.
    """

    fields = string.split(':')
    name = fields[0]
    opts = dict()
    for f in fields[1:]:
        k, v = f.split('=')
        opts[k] = v
    return name, opts

def init(args: list): 
    """
    Construct the metric objects, see `parse_args` for formatting instructions. 

    Parameters:

    args: a list of strings, each string configures one metric, see `parse_args`.
    """
    metrics = dict()
    for metric_cfg in args: 
        name, opts = parse_args(metric_cfg)
        if name == 'comet':
            import torch
            from telescope.metrics import COMET
            modelname = opts.get("modelname", "wmt21-small-da-152012")
            if opts.get("cuda", "false") == "false":
                torch.cuda.is_available = lambda: False
            comet = COMET(modelname=modelname)
            metrics[name] = comet
        elif name == 'cometinho':
            from comet import download_model, load_from_checkpoint
            modelname = opts.get("modelname", "wmt21-cometinho-da")
            if opts.get("cuda", "false") == "false":
                torch.cuda.is_available = lambda: False
            model_path = download_model(modelname)
            cometinho = load_from_checkpoint(model_path)
            metrics[name] = cometinho
        else:
            raise ValueError(f"You need to integrate metric '{name}'")
    return metrics

def handle_comet(comet, hyps, refs, srcs):
    """
    Compute segment scores using comet and return a list of scores (one score per segment)
    """
    return comet.score(srcs, hyps, refs).seg_scores


def handle_cometinho(cometinho, hyps, refs, srcs):
    """
    Compute segment scores using comet and return a list of scores (one score per segment)
    """
    data = [
        {'src': s, 'mt': h, 'ref': r} for h, r, s in zip(hyps, refs, srcs)
    ]
    seg_scores, sys_score = cometinho.predict(data, batch_size=8, gpus=1)
    return seg_scores


def score(metrics, hyps, refs, srcs, logger=None):
    """
    Evaluate a batch of segments using each of the configured metrics. 

    Parameters:
    
    metrics: a dictionary mapping a metric's name to a metric's object
    hyps: a list of N hypotheses
    refs: a list of N references (one per hypothesis)
    srcs: a list of N sources (one per hypothesis)

    Return a dictionary mapping a metric's name to a list with N scores (one per hypothesis).
    """
    results = dict()
    for name, metric in metrics.items():
        if name == 'comet':
            results[name] = handle_comet(metric, hyps, refs, srcs)
        elif name == 'cometinho':
            results[name] = handle_cometinho(metric, hyps, refs, srcs)
        else:
            raise ValueError(f"Unknown metric '{name}'")
    return results
