import t5
import os
import functools
import tensorflow as tf
# from t5.data import sentencepiece_vocabulary
from t5.evaluation import metrics

DATA_DIR = "./data/"


def get_downloaded_data_path(data_dir1, split, extension):
    return os.path.join(data_dir1, split + extension)

def normalize_text(text):
    """Lowercase and remove quotes from a TensorFlow string."""
    text = tf.strings.lower(text)
    text = tf.strings.regex_replace(text, "'(.*)'", r"\1")
    return text

def to_inputs_and_targets(ex):
    return {
        "inputs": normalize_text(ex["inputs"]),
        "targets": normalize_text(ex["targets"])
    }

def preprocess(
        dataset,
        prefix='',  # not used
        sample_answer=False,  # not used
):
    return dataset.map(to_inputs_and_targets,
        num_parallel_calls=tf.data.experimental.AUTOTUNE)


def dataset_fn(split, shuffle_files=False, dataset=""):
    # Load lines from the text file as examples.
    ds = tf.data.TextLineDataset(get_downloaded_data_path(DATA_DIR + dataset, split, ".tsv"))
    print(" >>>> about to read tsv . . . ")
    ds = ds.map(
        functools.partial(tf.io.decode_csv, record_defaults=["", "", ""], use_quote_delim=False, field_delim="\t"),
        num_parallel_calls=tf.data.experimental.AUTOTUNE)
    # Map each tuple to a {"question": ... "answers": ...} dict.
    ds = ds.map(lambda *ex: dict(zip(["inputs", "targets", "id"], ex)))
    return ds


def dataset_fn_two_column(split, shuffle_files=False, dataset=""):
    # Load lines from the text file as examples.
    ds = tf.data.TextLineDataset(get_downloaded_data_path(DATA_DIR + dataset, split, ".tsv"))
    print(" >>>> about to read tsv . . . ")
    ds = ds.map(
        functools.partial(tf.io.decode_csv, record_defaults=["", ""], use_quote_delim=False, field_delim="\t"),
        num_parallel_calls=tf.data.experimental.AUTOTUNE)
    # Map each tuple to a {"question": ... "answers": ...} dict.
    ds = ds.map(lambda *ex: dict(zip(["inputs", "targets"], ex)))
    return ds


def postprocessor(answer, example=None, is_target=False):
    """Returns answer, or all answers if the full example is provided."""
    if example:
        return tf.compat.as_text(answer) + "\t" + tf.compat.as_text(example["id"])
    else:
        return answer


def postprocessor_two_column(answer, example=None, is_target=False):
    """Returns answer, or all answers if the full example is provided."""
    return tf.compat.as_text(answer)



for task in [
    "ir1",
    "ir2",
    "ir3",
    "ir4"

]:
    t5.data.set_tfds_data_dir_override(DATA_DIR + task)
    t5.data.TaskRegistry.add(
        f"{task}_task",
        # Supply a function which returns a tf.data.Dataset.
        dataset_fn=functools.partial(dataset_fn_two_column, dataset=task),
        splits=["train", "test", "dev"],
        # Supply a function which preprocesses text from the tf.data.Dataset.
        text_preprocessor=preprocess,
        # Lowercase targets before computing metrics.
        postprocess_fn=postprocessor_two_column,
        # sentencepiece_model_path=t5.data.DEFAULT_SPM_PATH,
        metric_fns=[metrics.squad]
    )

    t5.data.MixtureRegistry.add(
        f"{task}_mixture", [f"{task}_task"], default_rate=1.0
    )
    
