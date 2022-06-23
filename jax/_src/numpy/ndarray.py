# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import abc
from typing import Any, Tuple, Optional, Union

from jax import core
from jax.interpreters import pxla
from jax._src import device_array
import numpy as np


class ArrayMeta(abc.ABCMeta):
  """Metaclass for overriding ndarray isinstance checks."""

  def __instancecheck__(self, instance):
    # Allow tracer instances with avals that are instances of UnshapedArray.
    # We could instead just declare Tracer an instance of the ndarray type, but
    # there can be traced values that are not arrays. The main downside here is
    # that isinstance(x, ndarray) might return true but
    # issubclass(type(x), ndarray) might return false for an array tracer.
    try:
      return (hasattr(instance, "aval") and
              isinstance(instance.aval, core.UnshapedArray))
    except AttributeError:
      super().__instancecheck__(instance)


class ndarray(metaclass=ArrayMeta):
  dtype: np.dtype
  ndim: int
  shape: Tuple[int, ...]
  size: int

  def __init__(self, shape, dtype=None, buffer=None, offset=0, strides=None,
               order=None):
    raise TypeError("jax.numpy.ndarray() should not be instantiated explicitly."
                    " Use jax.numpy.array, or jax.numpy.zeros instead.")

  @abc.abstractmethod
  def __getitem__(self, key, indices_are_sorted=False,
                  unique_indices=False) -> Any: ...
  @abc.abstractmethod
  def __setitem__(self, key, value) -> Any: ...
  @abc.abstractmethod
  def __len__(self) -> Any: ...
  @abc.abstractmethod
  def __iter__(self) -> Any: ...
  @abc.abstractmethod
  def __reversed__(self) -> Any: ...

  # Comparisons
  @abc.abstractmethod
  def __lt__(self, other) -> Any: ...
  @abc.abstractmethod
  def __le__(self, other) -> Any: ...
  @abc.abstractmethod
  def __eq__(self, other) -> Any: ...
  @abc.abstractmethod
  def __ne__(self, other) -> Any: ...
  @abc.abstractmethod
  def __gt__(self, other) -> Any: ...
  @abc.abstractmethod
  def __ge__(self, other) -> Any: ...

  # Unary arithmetic

  @abc.abstractmethod
  def __neg__(self) -> Any: ...
  @abc.abstractmethod
  def __pos__(self) -> Any: ...
  @abc.abstractmethod
  def __abs__(self) -> Any: ...
  @abc.abstractmethod
  def __invert__(self) -> Any: ...

  # Binary arithmetic

  @abc.abstractmethod
  def __add__(self, other) -> Any: ...
  @abc.abstractmethod
  def __sub__(self, other) -> Any: ...
  @abc.abstractmethod
  def __mul__(self, other) -> Any: ...
  @abc.abstractmethod
  def __matmul__(self, other) -> Any: ...
  @abc.abstractmethod
  def __truediv__(self, other) -> Any: ...
  @abc.abstractmethod
  def __floordiv__(self, other) -> Any: ...
  @abc.abstractmethod
  def __mod__(self, other) -> Any: ...
  @abc.abstractmethod
  def __divmod__(self, other) -> Any: ...
  @abc.abstractmethod
  def __pow__(self, other) -> Any: ...
  @abc.abstractmethod
  def __lshift__(self, other) -> Any: ...
  @abc.abstractmethod
  def __rshift__(self, other) -> Any: ...
  @abc.abstractmethod
  def __and__(self, other) -> Any: ...
  @abc.abstractmethod
  def __xor__(self, other) -> Any: ...
  @abc.abstractmethod
  def __or__(self, other) -> Any: ...

  @abc.abstractmethod
  def __radd__(self, other) -> Any: ...
  @abc.abstractmethod
  def __rsub__(self, other) -> Any: ...
  @abc.abstractmethod
  def __rmul__(self, other) -> Any: ...
  @abc.abstractmethod
  def __rmatmul__(self, other) -> Any: ...
  @abc.abstractmethod
  def __rtruediv__(self, other) -> Any: ...
  @abc.abstractmethod
  def __rfloordiv__(self, other) -> Any: ...
  @abc.abstractmethod
  def __rmod__(self, other) -> Any: ...
  @abc.abstractmethod
  def __rdivmod__(self, other) -> Any: ...
  @abc.abstractmethod
  def __rpow__(self, other) -> Any: ...
  @abc.abstractmethod
  def __rlshift__(self, other) -> Any: ...
  @abc.abstractmethod
  def __rrshift__(self, other) -> Any: ...
  @abc.abstractmethod
  def __rand__(self, other) -> Any: ...
  @abc.abstractmethod
  def __rxor__(self, other) -> Any: ...
  @abc.abstractmethod
  def __ror__(self, other) -> Any: ...

  @abc.abstractmethod
  def __bool__(self) -> Any: ...
  @abc.abstractmethod
  def __complex__(self) -> Any: ...
  @abc.abstractmethod
  def __int__(self) -> Any: ...
  @abc.abstractmethod
  def __float__(self) -> Any: ...
  @abc.abstractmethod
  def __round__(self, ndigits=None) -> Any: ...

  @abc.abstractmethod
  def __index__(self) -> Any: ...

  # np.ndarray methods:
  @abc.abstractmethod
  def all(self, axis: Optional[Union[int, Tuple[int, ...]]] = None, out=None,
          keepdims=None) -> Any: ...
  @abc.abstractmethod
  def any(self, axis: Optional[Union[int, Tuple[int, ...]]] = None, out=None,
          keepdims=None) -> Any: ...
  @abc.abstractmethod
  def argmax(self, axis: Optional[int] = None, out=None, keepdims=None) -> Any: ...
  @abc.abstractmethod
  def argmin(self, axis: Optional[int] = None, out=None, keepdims=None) -> Any: ...
  @abc.abstractmethod
  def argpartition(self, kth, axis=-1, kind='introselect', order=None) -> Any: ...
  @abc.abstractmethod
  def argsort(self, axis: Optional[int] = -1, kind='quicksort', order=None) -> Any: ...
  @abc.abstractmethod
  def astype(self, dtype) -> Any: ...
  @abc.abstractmethod
  def choose(self, choices, out=None, mode='raise') -> Any: ...
  @abc.abstractmethod
  def clip(self, a_min=None, a_max=None, out=None) -> Any: ...
  @abc.abstractmethod
  def compress(self, condition, axis: Optional[int] = None, out=None) -> Any: ...
  @abc.abstractmethod
  def conj(self) -> Any: ...
  @abc.abstractmethod
  def conjugate(self) -> Any: ...
  @abc.abstractmethod
  def copy(self) -> Any: ...
  @abc.abstractmethod
  def cumprod(self, axis: Optional[Union[int, Tuple[int, ...]]] = None,
              dtype=None, out=None) -> Any: ...
  @abc.abstractmethod
  def cumsum(self, axis: Optional[Union[int, Tuple[int, ...]]] = None,
             dtype=None, out=None) -> Any: ...
  @abc.abstractmethod
  def diagonal(self, offset=0, axis1: int = 0, axis2: int = 1) -> Any: ...
  @abc.abstractmethod
  def dot(self, b, *, precision=None) -> Any: ...
  @abc.abstractmethod
  def flatten(self) -> Any: ...
  @property
  @abc.abstractmethod
  def imag(self) -> Any: ...
  @abc.abstractmethod
  def item(self, *args) -> Any: ...
  @abc.abstractmethod
  def max(self, axis: Optional[Union[int, Tuple[int, ...]]] = None, out=None,
          keepdims=None, initial=None, where=None) -> Any: ...
  @abc.abstractmethod
  def mean(self, axis: Optional[Union[int, Tuple[int, ...]]] = None, dtype=None,
           out=None, keepdims=False, *, where=None,) -> Any: ...
  @abc.abstractmethod
  def min(self, axis: Optional[Union[int, Tuple[int, ...]]] = None, out=None,
          keepdims=None, initial=None, where=None) -> Any: ...
  @property
  @abc.abstractmethod
  def nbytes(self) -> Any: ...
  @abc.abstractmethod
  def nonzero(self, *, size=None, fill_value=None) -> Any: ...
  @abc.abstractmethod
  def prod(self, axis: Optional[Union[int, Tuple[int, ...]]] = None, dtype=None,
           out=None, keepdims=None, initial=None, where=None) -> Any: ...
  @abc.abstractmethod
  def ptp(self, axis: Optional[Union[int, Tuple[int, ...]]] = None, out=None,
          keepdims=False,) -> Any: ...
  @abc.abstractmethod
  def ravel(self, order='C') -> Any: ...
  @property
  @abc.abstractmethod
  def real(self) -> Any: ...
  @abc.abstractmethod
  def repeat(self, repeats, axis: Optional[int] = None, *,
             total_repeat_length=None) -> Any: ...
  @abc.abstractmethod
  def reshape(self, *args, order='C') -> Any: ...
  @abc.abstractmethod
  def round(self, decimals=0, out=None) -> Any: ...
  @abc.abstractmethod
  def searchsorted(self, v, side='left', sorter=None) -> Any: ...
  @abc.abstractmethod
  def sort(self, axis: Optional[int] = -1, kind='quicksort', order=None) -> Any: ...
  @abc.abstractmethod
  def squeeze(self, axis: Optional[Union[int, Tuple[int, ...]]] = None) -> Any: ...
  @abc.abstractmethod
  def std(self, axis: Optional[Union[int, Tuple[int, ...]]] = None,
          dtype=None, out=None, ddof=0, keepdims=False, *, where=None) -> Any: ...
  @abc.abstractmethod
  def sum(self, axis: Optional[Union[int, Tuple[int, ...]]] = None, dtype=None,
          out=None, keepdims=None, initial=None, where=None) -> Any: ...
  @abc.abstractmethod
  def swapaxes(self, axis1: int, axis2: int) -> Any: ...
  @abc.abstractmethod
  def take(self, indices, axis: Optional[int] = None, out=None,
           mode=None) -> Any: ...
  @abc.abstractmethod
  def tobytes(self, order='C') -> Any: ...
  @abc.abstractmethod
  def tolist(self) -> Any: ...
  @abc.abstractmethod
  def trace(self, offset=0, axis1: int = 0, axis2: int = 1, dtype=None,
            out=None) -> Any: ...
  @abc.abstractmethod
  def transpose(self, *args) -> Any: ...
  @abc.abstractmethod
  def var(self, axis: Optional[Union[int, Tuple[int, ...]]] = None,
          dtype=None, out=None, ddof=0, keepdims=False, *, where=None) -> Any: ...
  @abc.abstractmethod
  def view(self, dtype=None, type=None) -> Any: ...

  # Even though we don't always support the NumPy array protocol, e.g., for
  # tracer types, for type checking purposes we must declare support so we
  # implement the NumPy ArrayLike protocol.
  def __array__(self) -> Any: ...

  # JAX extensions
  @property
  @abc.abstractmethod
  def at(self) -> Any: ...
  @property
  @abc.abstractmethod
  def aval(self) -> Any: ...
  @property
  @abc.abstractmethod
  def weak_type(self) -> bool: ...


ndarray.register(device_array.DeviceArray)
for t in device_array.device_array_types:
  ndarray.register(t)
ndarray.register(pxla._SDA_BASE_CLASS)
