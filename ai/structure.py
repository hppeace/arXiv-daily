from pydantic import BaseModel, Field

class Structure(BaseModel):
    tldr: str = Field(
        description="A concise one- or two-sentence summary highlighting the paper's core contribution or finding."
    )
    motivation: str = Field(
        description="What problem, limitation, or research gap the paper aims to solve or explore."
    )
    method: str = Field(
        description="The key techniques, algorithms, model architectures, or approaches proposed or used in the paper."
    )
    result: str = Field(
        description="The main experimental results, benchmarks, quantitative findings, or qualitative outcomes."
    )
    conclusion: str = Field(
        description="The major insights, implications, or future directions derived from the study."
    )
