from typing import Any, Optional, Type, TypeVar, Union

import numpy as np

from docarray.base_document import BaseDocument
from docarray.typing import AnyEmbedding, AudioUrl
from docarray.typing.bytes.audio_bytes import AudioBytes
from docarray.typing.tensor.abstract_tensor import AbstractTensor
from docarray.typing.tensor.audio.audio_tensor import AudioTensor
from docarray.utils.misc import is_tf_available, is_torch_available

torch_available = is_torch_available()
if torch_available:
    import torch

tf_available = is_tf_available()
if tf_available:
    import tensorflow as tf  # type: ignore


T = TypeVar('T', bound='Audio')


class Audio(BaseDocument):
    """
    Document for handling audios.

    The Audio Document can contain an AudioUrl (`Audio.url`), an AudioTensor
    (`Audio.tensor`), and an AnyEmbedding (`Audio.embedding`).

    EXAMPLE USAGE:

    You can use this Document directly:

    .. code-block:: python

        from docarray.documents import Audio

        # use it directly
        audio = Audio(
            url='https://github.com/docarray/docarray/blob/feat-rewrite-v2/tests/toydata/hello.wav?raw=true'
        )
        audio.tensor = audio.url.load()
        model = MyEmbeddingModel()
        audio.embedding = model(audio.tensor)

    You can extend this Document:

    .. code-block:: python

        from docarray.documents import Audio, Text
        from typing import Optional

        # extend it
        class MyAudio(Audio):
            name: Optional[Text]


        audio = MyAudio(
            url='https://github.com/docarray/docarray/blob/feat-rewrite-v2/tests/toydata/hello.wav?raw=true'
        )
        audio.tensor = audio.url.load()
        model = MyEmbeddingModel()
        audio.embedding = model(audio.tensor)
        audio.name = Text(text='my first audio')


    You can use this Document for composition:

    .. code-block:: python

        from docarray import BaseDocument
        from docarray.documents import Audio, Text

        # compose it
        class MultiModalDoc(Document):
            audio: Audio
            text: Text


        mmdoc = MultiModalDoc(
            audio=Audio(
                url='https://github.com/docarray/docarray/blob/feat-rewrite-v2/tests/toydata/hello.wav?raw=true'
            ),
            text=Text(text='hello world, how are you doing?'),
        )
        mmdoc.audio.tensor = mmdoc.audio.url.load()

        # equivalent to

        mmdoc.audio.bytes = mmdoc.audio.url.load_bytes()

        mmdoc.audio.tensor = mmdoc.audio.bytes.load()

    """

    url: Optional[AudioUrl]
    tensor: Optional[AudioTensor]
    embedding: Optional[AnyEmbedding]
    bytes: Optional[AudioBytes]

    @classmethod
    def validate(
        cls: Type[T],
        value: Union[str, AbstractTensor, Any],
    ) -> T:
        if isinstance(value, str):
            value = cls(url=value)
        elif isinstance(value, (AbstractTensor, np.ndarray)) or (
            torch_available
            and isinstance(value, torch.Tensor)
            or (tf_available and isinstance(value, tf.Tensor))
        ):
            value = cls(tensor=value)

        return super().validate(value)