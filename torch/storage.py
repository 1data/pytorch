import torch
from ._utils import _type, _range


class _StorageBase(object):
    is_cuda = False

    def __str__(self):
        content = ' ' + '\n '.join(str(self[i]) for i in _range(len(self)))
        return content + '\n[{} of size {}]'.format(torch.typename(self), len(self))

    def __repr__(self):
        return str(self)

    def __iter__(self):
        return iter(map(lambda i: self[i], _range(self.size())))

    def copy_(self, source, async=False):
        if async:
            torch._C._storageCopyAsync(self, source)
        else:
            torch._C._storageCopy(self, source)
        return self

    def __copy__(self):
        return self.clone()

    def __deepcopy__(self, memo):
        memo = memo.setdefault('torch', {})
        if self._cdata in memo:
            return memo[self._cdata]
        new_storage = self.clone()
        memo[self._cdata] = new_storage
        return new_storage

    def __reduce__(self):
        return type(self), (self.tolist(),)

    def clone(self):
        return type(self)(self.size()).copy_(self)

    def tolist(self):
        return [v for v in self]

    def double(self, async=False):
        return self.type(type(self).__module__ + '.DoubleStorage', async)

    def float(self, async=False):
        return self.type(type(self).__module__ + '.FloatStorage', async)

    def long(self, async=False):
        return self.type(type(self).__module__ + '.LongStorage', async)

    def int(self, async=False):
        return self.type(type(self).__module__ + '.IntStorage', async)

    def short(self, async=False):
        return self.type(type(self).__module__ + '.ShortStorage', async)

    def char(self, async=False):
        return self.type(type(self).__module__ + '.CharStorage', async)

    def byte(self, async=False):
        return self.type(type(self).__module__ + '.ByteStorage', async)


_StorageBase.type = _type