from kfp import dsl, compiler
from google.cloud import aiplatform as aip

PROJECT_ID = 'cookthis-400019'
REGION="us-west4"
BUCKET_NAME = "saved_predictions"
PIPELINE_ROOT = f"gs://{BUCKET_NAME}/pipeline_root/"
DISPLAY_NAME = "test"

# Define Components
@dsl.component
def square(x: float) -> float:
    return x**2

@dsl.component
def add(x: float, y: float) -> float:
    return x + y

@dsl.component
def square_root(x: float) -> float:
    return x**0.5
# Define Pipeline

@dsl.pipeline
def sample_pipeline(a: float = 3.0, b: float = 4.0) -> float:
    a_sq_task = square(x=a)
    b_sq_task = square(x=b)
    sum_task = add(x=a_sq_task.output, y=b_sq_task.output)
    return square_root(x=sum_task.output).output


# Build yaml file for pipeline
compiler.Compiler().compile(sample_pipeline, package_path="test.yaml")

job = aip.PipelineJob(
    display_name=DISPLAY_NAME,
    template_path="test.yaml",
    pipeline_root=PIPELINE_ROOT,
    enable_caching=False,
)

job.run()

# import kfp

# from kfp.v2 import compiler, dsl
# from kfp.v2.dsl import component, pipeline, Artifact, ClassificationMetrics, Input, Output, Model, Metrics

# from google.cloud import aiplatform_v1 as aiplatform
# from google_cloud_pipeline_components import aiplatform as gcc_aip
# from typing import NamedTuple

# PROJECT_ID = 'cookthis-400019'
# REGION="us-west4"
# BUCKET_NAME = "saved_predictions"
# PIPELINE_ROOT = f"{BUCKET_NAME}/pipeline_root/"

# @component(base_image="python:3.9", output_component_file="first-component.yaml")
# def product_name(text: str) -> str:
#     return text

# @component(packages_to_install=["emoji"])
# def emoji(
#     text: str,
# ) -> NamedTuple(
#     "Outputs",
#     [
#         ("emoji_text", str),  # Return parameters
#         ("emoji", str),
#     ],
# ):
#     import emoji

#     emoji_text = text
#     emoji_str = emoji.emojize(':' + emoji_text + ':', language='alias')
#     print("output one: {}; output_two: {}".format(emoji_text, emoji_str))
#     return (emoji_text, emoji_str)

# @component
# def build_sentence(
#     product: str,
#     emoji: str,
#     emojitext: str
# ) -> str:
#     print("We completed the pipeline, hooray!")
#     end_str = product + " is "
#     if len(emoji) > 0:
#         end_str += emoji
#     else:
#         end_str += emojitext
#     return(end_str)

# @pipeline(
#     name="hello-world",
#     description="An intro pipeline",
#     pipeline_root=PIPELINE_ROOT,
# )

# # You can change the `text` and `emoji_str` parameters here to update the pipeline output
# def intro_pipeline(text: str = "Vertex Pipelines", emoji_str: str = "sparkles"):
#     product_task = product_name(text)
#     emoji_task = emoji(emoji_str)
#     consumer_task = build_sentence(
#         product_task.output,
#         emoji_task.outputs["emoji"],
#         emoji_task.outputs["emoji_text"],
#     )

# compiler.Compiler().compile(
#     pipeline_func=intro_pipeline, package_path="intro_pipeline_job.json"
# )

# from datetime import datetime

# TIMESTAMP = datetime.now().strftime("%Y%m%d%H%M%S")

# job = aiplatform.PipelineJob(
#     display_name="hello-world-pipeline",
#     template_path="intro_pipeline_job.json",
#     job_id="hello-world-pipeline-{0}".format(TIMESTAMP),
#     enable_caching=True
# )

# job.submit()
