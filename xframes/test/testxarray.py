import unittest
import math
import os

# python testxarray.py
# python -m unittest testxarray
# python -m unittest testxarray.TestXArrayVersion
# python -m unittest testxarray.TestXArrayVersion.test_version

from xframes import XArray


def eq_list(expected, result):
    return expected == list(result)

class TestXArrayVersion(unittest.TestCase):
    """
    Tests XArray version
    """

    def test_version(self):
        ver = XArray.version()
        self.assertEqual(str, type(ver))


class TestXArrayConstructorLocal(unittest.TestCase):
    """
    Tests XArray constructors that create data from local sources.
    """

    def test_construct_list_int_infer(self):
        t = XArray([1, 2, 3])
        self.assertEqual(3, len(t))
        self.assertEqual(1, t[0])
        self.assertEqual(int, t.dtype())

    def test_construct_list_int(self):
        t = XArray([1, 2, 3], dtype=int)
        self.assertEqual(3, len(t))
        self.assertEqual(1, t[0])
        self.assertEqual(int, t.dtype())

    def test_construct_list_str_infer(self):
        t = XArray(['a', 'b', 'c'])
        self.assertEqual(3, len(t))
        self.assertEqual('a', t[0])
        self.assertEqual(str, t.dtype())

    def test_construct_list_str(self):
        t = XArray([1, 2, 3], dtype=str)
        self.assertEqual(3, len(t))
        self.assertEqual('1', t[0])
        self.assertEqual(str, t.dtype())

    def test_construct_list_float_infer(self):
        t = XArray([1.0, 2.0, 3.0])
        self.assertEqual(3, len(t))
        self.assertEqual(1.0, t[0])
        self.assertEqual(float, t.dtype())

    def test_construct_list_float(self):
        t = XArray([1, 2, 3], dtype=float)
        self.assertEqual(3, len(t))
        self.assertEqual(1.0, t[0])
        self.assertEqual(float, t.dtype())

    def test_construct_list_bool_infer(self):
        t = XArray([True, False])
        self.assertEqual(2, len(t))
        self.assertEqual(True, t[0])
        self.assertEqual(bool, t.dtype())

    def test_construct_list_bool(self):
        t = XArray([True, False], dtype=bool)
        self.assertEqual(2, len(t))
        self.assertEqual(True, t[0])
        self.assertEqual(bool, t.dtype())

    def test_construct_list_list_infer(self):
        t = XArray([[1, 2, 3], [10]])
        self.assertEqual(2, len(t))
        self.assertEqual([1, 2, 3], t[0])
        self.assertEqual([10], t[1])
        self.assertEqual(list, t.dtype())

    def test_construct_list_list(self):
        t = XArray([[1, 2, 3], [10]], dtype=list)
        self.assertEqual(2, len(t))
        self.assertEqual([1, 2, 3], t[0])
        self.assertEqual([10], t[1])
        self.assertEqual(list, t.dtype())

    def test_construct_list_dict_infer(self):
        t = XArray([{'a': 1, 'b': 2}, {'x': 10}])
        self.assertEqual(2, len(t))
        self.assertEqual({'a': 1, 'b': 2}, t[0])
        self.assertEqual(dict, t.dtype())

    def test_construct_list_dict(self):
        t = XArray([{'a': 1, 'b': 2}, {'x': 10}], dtype=dict)
        self.assertEqual(2, len(t))
        # TODO does this actually work ?
        self.assertEqual({'a': 1, 'b': 2}, t[0])
        self.assertEqual(dict, t.dtype())

    def test_construct_empty_list_infer(self):
        t = XArray([])
        self.assertEqual(0, len(t))
        self.assertEqual(None, t.dtype())
    
    def test_construct_empty_list(self):
        t = XArray([], dtype=int)
        self.assertEqual(0, len(t))
        self.assertEqual(int, t.dtype())

    def test_construct_list_int_cast_fail(self):
        with self.assertRaises(ValueError):
            t = XArray(['a', 'b', 'c'], dtype=int)
            print t     # force materialization

    def test_construct_list_int_cast_ignore(self):
        t = XArray(['1', '2', 'c'], dtype=int, ignore_cast_failure=True)
        self.assertEqual(3, len(t))
        self.assertEqual(1, t[0])
        self.assertEqual(None, t[2])
        self.assertEqual(int, t.dtype())


class TestXArrayConstructorRange(unittest.TestCase):
    """ 
    Tests XArray constructors for sequential ranges.
    """

    def test_construct_none(self):
        with self.assertRaises(TypeError):
            XArray.from_sequence()

    def test_construct_nonint_stop(self):
        with self.assertRaises(TypeError):
            XArray.from_sequence(1.0)

    def test_construct_nonint_start(self):
        with self.assertRaises(TypeError):
            XArray.from_sequence(1.0, 10.0)

    def test_construct_stop(self):
        t = XArray.from_sequence(100, 200)
        self.assertEqual(100, len(t))
        self.assertEqual(100, t[0])
        self.assertEqual(int, t.dtype())

    def test_construct_start(self):
        t = XArray.from_sequence(100)
        self.assertEqual(100, len(t))
        self.assertEqual(0, t[0])
        self.assertEqual(int, t.dtype())


class TestXArrayConstructFromRdd(unittest.TestCase):
    """ 
    Tests XArray from_rdd class method
    """

    def test_construct_from_rdd(self):
        # TODO
        pass


class TestXArrayConstructorLoad(unittest.TestCase):
    """ 
    Tests XArray constructors that loads from file.
    """

    def test_construct_local_file_int(self):
        t = XArray('files/test-array-int')
        self.assertEqual(4, len(t))
        self.assertEqual(int, t.dtype())
        self.assertEqual(1, t[0])

    def test_construct_local_file_float(self):
        t = XArray('files/test-array-float')
        self.assertEqual(4, len(t))
        self.assertEqual(float, t.dtype())
        self.assertEqual(1.0, t[0])

    def test_construct_local_file_str(self):
        t = XArray('files/test-array-str')
        self.assertEqual(4, len(t))
        self.assertEqual(str, t.dtype())
        self.assertEqual('a', t[0])

    def test_construct_local_file_list(self):
        t = XArray('files/test-array-list')
        self.assertEqual(4, len(t))
        self.assertEqual(list, t.dtype())
        self.assertEqual([1, 2], t[0])

    def test_construct_local_file_dict(self):
        t = XArray('files/test-array-dict')
        self.assertEqual(4, len(t))
        self.assertEqual(dict, t.dtype())
        self.assertEqual({1: 'a', 2: 'b'}, t[0])


class TestXArrayFromConst(unittest.TestCase):
    """ 
    Tests XArray constructed from const.
    """

    def test_from_const_int(self):
        t = XArray.from_const(1, 10)
        self.assertEqual(10, len(t))
        self.assertEqual(1, t[0])
        self.assertEqual(int, t.dtype())

    def test_from_const_float(self):
        t = XArray.from_const(1.0, 10)
        self.assertEqual(10, len(t))
        self.assertEqual(1.0, t[0])
        self.assertEqual(float, t.dtype())

    def test_from_const_str(self):
        t = XArray.from_const('a', 10)
        self.assertEqual(10, len(t))
        self.assertEqual('a', t[0])
        self.assertEqual(str, t.dtype())

    def test_from_const_list(self):
        t = XArray.from_const([1, 2], 10)
        self.assertEqual(10, len(t))
        self.assertEqual([1, 2], t[0])
        self.assertEqual(list, t.dtype())

    def test_from_const_dict(self):
        t = XArray.from_const({1: 'a'}, 10)
        self.assertEqual(10, len(t))
        self.assertEqual({1: 'a'}, t[0])
        self.assertEqual(dict, t.dtype())

    def test_from_const_negint(self):
        with self.assertRaises(ValueError):
            XArray.from_const(1, -10)

    def test_from_const_nonint(self):
        with self.assertRaises(TypeError):
            XArray.from_const(1, 'a')

    def test_from_const_bad_type(self):
        with self.assertRaises(TypeError):
            XArray.from_const(True, 10)


class TestXArraySaveBinary(unittest.TestCase):
    """ 
    Tests XArray save binary format
    """
    def test_save(self):
        t = XArray([1, 2, 3])
        path = 'tmp/array-binary'
        t.save(path)
        success_path = os.path.join(path, '_SUCCESS')
        self.assertTrue(os.path.isfile(success_path))

    def test_save_format(self):
        t = XArray([1, 2, 3])
        path = 'tmp/array-binary'
        t.save(path, format='binary')
        success_path = os.path.join(path, '_SUCCESS')
        self.assertTrue(os.path.isfile(success_path))


class TestXArraySaveText(unittest.TestCase):
    """ 
    Tests XArray save text format
    """
    def test_save(self):
        t = XArray([1, 2, 3])
        path = 'tmp/array-text.txt'
        t.save(path)
        success_path = os.path.join(path, '_SUCCESS')
        self.assertTrue(os.path.isfile(success_path))

    def test_save_format(self):
        t = XArray([1, 2, 3])
        path = 'tmp/array-text'
        t.save(path, format='text')
        success_path = os.path.join(path, '_SUCCESS')
        self.assertTrue(os.path.isfile(success_path))

class TestXArraySaveCsv(unittest.TestCase):
    """
    Tests XArray save csv format
    """
    def test_save(self):
        t = XArray([1, 2, 3])
        path = 'tmp/array-csv.csv'
        t.save(path)
        with open(path) as f:
            self.assertEqual('1', f.readline().strip())
            self.assertEqual('2', f.readline().strip())
            self.assertEqual('3', f.readline().strip())

    def test_save_format(self):
        t = XArray([1, 2, 3])
        path = 'tmp/array-csv'
        t.save(path, format='csv')
        with open(path) as f:
            self.assertEqual('1', f.readline().strip())
            self.assertEqual('2', f.readline().strip())
            self.assertEqual('3', f.readline().strip())


class TestXArrayRepr(unittest.TestCase):
    """ 
    Tests XArray __repr__ function.
    """
    def test_repr(self):
        t = XArray([1, 2, 3])
        s = t.__repr__()
        self.assertEqual("""dtype: <type 'int'>
Rows: 3
[1, 2, 3]""", s)


class TestXArrayStr(unittest.TestCase):
    """ 
    Tests XArray __str__ function.
    """
    def test_str(self):
        t = XArray(range(200))
        s = t.__repr__()
        self.assertEqual("dtype: <type 'int'>\nRows: 200\n[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11," +
                         " 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25," +
                         " 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41," +
                         " 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57," +
                         " 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73," +
                         " 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90," +
                         " 91, 92, 93, 94, 95, 96, 97, 98, 99, ... ]", s)


class TestXArrayNonzero(unittest.TestCase):
    """ 
    Tests XArray __nonzero__ function
    """
    def test_nonzero_nonzero(self):
        t = XArray([0])
        self.assertTrue(bool(t))

    def test_nonzero_zero(self):
        t = XArray([])
        self.assertFalse(bool(t))


class TestXArrayLen(unittest.TestCase):
    """ 
    Tests XArray __len__ function
    """
    def test_len_nonzero(self):
        t = XArray([0])
        self.assertEqual(1, len(t))

    def test_len_zero(self):
        t = XArray([])
        self.assertEqual(0, len(t))


class TestXArrayIterator(unittest.TestCase):
    """ 
    Tests XArray iteration function
    """
    def test_iter_empty(self):
        t = XArray([])
        for _ in t:
            self.assertEquals(False, True, 'should not iterate')

    def test_iter_1(self):
        t = XArray([0])
        for elem in t:
            self.assertEquals(0, elem)

    def test_iter_3(self):
        t = XArray([0, 1, 2])
        for elem, expect in zip(t, [0, 1, 2]):
            self.assertEquals(expect, elem)


class TestXArrayAddScalar(unittest.TestCase):
    """ 
    Tests XArray Scalar Addition
    """
    # noinspection PyAugmentAssignment
    def test_add_scalar(self):
        t = XArray([1, 2, 3])
        self.assertEqual(3, len(t))
        self.assertEqual(1, t[0])
        self.assertEqual(int, t.dtype())
        t = t + 2
        self.assertEqual(3, t[0])
        self.assertEqual(4, t[1])
        self.assertEqual(5, t[2])


class TestXArrayAddVector(unittest.TestCase):
    """ 
    Tests XArray Vector Addition
    """
    def test_add_vector(self):
        t1 = XArray([1, 2, 3])
        t2 = XArray([4, 5, 6])
        t = t1 + t2
        self.assertEqual(3, len(t))
        self.assertEqual(int, t.dtype())
        self.assertEqual(5, t[0])
        self.assertEqual(7, t[1])
        self.assertEqual(9, t[2])

    def test_add_vector_safe(self):
        t1 = XArray([1, 2, 3])
        t = t1 + t1
        self.assertEqual(3, len(t))
        self.assertEqual(int, t.dtype())
        self.assertEqual(2, t[0])
        self.assertEqual(4, t[1])
        self.assertEqual(6, t[2])

        
class TestXArrayOpScalar(unittest.TestCase):
    """ 
    Tests XArray Scalar operations other than addition
    """
    def test_sub_scalar(self):
        t = XArray([1, 2, 3])
        res = t - 1
        self.assertEqual(0, res[0])
        self.assertEqual(1, res[1])
        self.assertEqual(2, res[2])

    def test_mul_scalar(self):
        t = XArray([1, 2, 3])
        res = t * 2
        self.assertEqual(2, res[0])
        self.assertEqual(4, res[1])
        self.assertEqual(6, res[2])

    def test_div_scalar(self):
        t = XArray([1, 2, 3])
        res = t / 2
        self.assertEqual(0, res[0])
        self.assertEqual(1, res[1])
        self.assertEqual(1, res[2])

    def test_pow_scalar(self):
        t = XArray([1, 2, 3])
        res = t ** 2
        self.assertEqual(1, res[0])
        self.assertEqual(4, res[1])
        self.assertEqual(9, res[2])

    def test_lt_scalar(self):
        t = XArray([1, 2, 3])
        res = t < 3
        self.assertEqual(True, res[0])
        self.assertEqual(True, res[1])
        self.assertEqual(False, res[2])

    def test_le_scalar(self):
        t = XArray([1, 2, 3])
        res = t <= 2
        self.assertEqual(True, res[0])
        self.assertEqual(True, res[1])
        self.assertEqual(False, res[2])

    def test_gt_scalar(self):
        t = XArray([1, 2, 3])
        res = t > 2
        self.assertEqual(False, res[0])
        self.assertEqual(False, res[1])
        self.assertEqual(True, res[2])

    def test_ge_scalar(self):
        t = XArray([1, 2, 3])
        res = t >= 3
        self.assertEqual(False, res[0])
        self.assertEqual(False, res[1])
        self.assertEqual(True, res[2])

    def test_radd_scalar(self):
        t = XArray([1, 2, 3])
        res = 1 + t
        self.assertEqual(2, res[0])
        self.assertEqual(3, res[1])
        self.assertEqual(4, res[2])

    def test_rsub_scalar(self):
        t = XArray([1, 2, 3])
        res = 1 - t
        self.assertEqual(0, res[0])
        self.assertEqual(-1, res[1])
        self.assertEqual(-2, res[2])

    def test_rmul_scalar(self):
        t = XArray([1, 2, 3])
        res = 2 * t
        self.assertEqual(2, res[0])
        self.assertEqual(4, res[1])
        self.assertEqual(6, res[2])

    def test_rdiv_scalar(self):
        t = XArray([1, 2, 3])
        res = 12 / t
        self.assertEqual(12, res[0])
        self.assertEqual(6, res[1])
        self.assertEqual(4, res[2])

    def test_eq_scalar(self):
        t = XArray([1, 2, 3])
        res = t == 2
        self.assertFalse(res[0])
        self.assertTrue(res[1])
        self.assertFalse(res[2])

    def test_ne_scalar(self):
        t = XArray([1, 2, 3])
        res = t != 2
        self.assertTrue(res[0])
        self.assertFalse(res[1])
        self.assertTrue(res[2])

    def test_and_scalar(self):
        t = XArray([1, 2, 3])
        with self.assertRaises(TypeError):
            _ = t & True

    def test_or_scalar(self):
        t = XArray([1, 2, 3])
        with self.assertRaises(TypeError):
            _ = t | False


# noinspection PyUnresolvedReferences
class TestXArrayOpVector(unittest.TestCase):
    """ 
    Tests XArray Vector operations other than addition
    """
    def test_sub_vector(self):
        t1 = XArray([1, 2, 3])
        t2 = XArray([4, 5, 6])
        t = t2 - t1
        self.assertEqual(3, t[0])
        self.assertEqual(3, t[1])
        self.assertEqual(3, t[2])

    def test_mul_vector(self):
        t1 = XArray([1, 2, 3])
        t2 = XArray([4, 5, 6])
        res = t1 * t2
        self.assertEqual(4, res[0])
        self.assertEqual(10, res[1])
        self.assertEqual(18, res[2])

    def test_div_vector(self):
        t1 = XArray([1, 2, 3])
        t2 = XArray([4, 6, 12])
        res = t2 / t1
        self.assertEqual(4, res[0])
        self.assertEqual(3, res[1])
        self.assertEqual(4, res[2])

    def test_lt_vector(self):
        t1 = XArray([1, 2, 3])
        t2 = XArray([4, 2, 2])
        res = t1 < t2
        self.assertEqual(True, res[0])
        self.assertEqual(False, res[1])
        self.assertEqual(False, res[2])

    def test_le_vector(self):
        t1 = XArray([1, 2, 3])
        t2 = XArray([4, 2, 2])
        res = t1 <= t2
        self.assertEqual(True, res[0])
        self.assertEqual(True, res[1])
        self.assertEqual(False, res[2])

    def test_gt_vector(self):
        t1 = XArray([1, 2, 3])
        t2 = XArray([4, 2, 2])
        res = t1 > t2
        self.assertEqual(False, res[0])
        self.assertEqual(False, res[1])
        self.assertEqual(True, res[2])

    def test_ge_vector(self):
        t1 = XArray([1, 2, 3])
        t2 = XArray([4, 2, 2])
        res = t1 >= t2
        self.assertEqual(False, res[0])
        self.assertEqual(True, res[1])
        self.assertEqual(True, res[2])

    def test_eq_vector(self):
        t1 = XArray([1, 2, 3])
        t2 = XArray([4, 2, 2])
        res = t1 == t2
        self.assertFalse(res[0])
        self.assertTrue(res[1])
        self.assertFalse(res[2])

    def test_ne_vector(self):
        t1 = XArray([1, 2, 3])
        t2 = XArray([4, 2, 2])
        res = t1 != t2
        self.assertTrue(res[0])
        self.assertFalse(res[1])
        self.assertTrue(res[2])

    def test_and_vector(self):
        t1 = XArray([0, 0, 1])
        t2 = XArray([0, 1, 1])
        res = t1 & t2
        self.assertEqual(0, res[0])
        self.assertEqual(0, res[1])
        self.assertEqual(1, res[2])

    def test_or_vector(self):
        t1 = XArray([0, 0, 1])
        t2 = XArray([0, 1, 1])
        res = t1 | t2
        self.assertEqual(0, res[0])
        self.assertEqual(1, res[1])
        self.assertEqual(1, res[2])


class TestXArrayOpUnary(unittest.TestCase):
    """ 
    Tests XArray Unary operations
    """
    def test_neg_unary(self):
        t = XArray([1, -2, 3])
        res = -t
        self.assertEqual(-1, res[0])
        self.assertEqual(2, res[1])
        self.assertEqual(-3, res[2])

    def test_pos_unary(self):
        t = XArray([1, -2, 3])
        res = +t
        self.assertEqual(1, res[0])
        self.assertEqual(-2, res[1])
        self.assertEqual(3, res[2])

    def test_abs_unary(self):
        t = XArray([1, -2, 3])
        res = abs(t)
        self.assertEqual(1, res[0])
        self.assertEqual(2, res[1])
        self.assertEqual(3, res[2])


class TestXArrayLogicalFilter(unittest.TestCase):
    """ 
    Tests XArray logical filter (XArray indexed by XArray)
    """
    def test_logical_filter_array(self):
        t1 = XArray([1, 2, 3])
        t2 = XArray([1, 0, 1])
        res = t1[t2]
        self.assertEqual(2, len(res))
        self.assertEqual(1, res[0])
        self.assertEqual(3, res[1])

    def test_logical_filter_test(self):
        t1 = XArray([1, 2, 3])
        res = t1[t1 != 2]
        self.assertEqual(2, len(res))
        self.assertEqual(1, res[0])
        self.assertEqual(3, res[1])

    def test_logical_filter_len_error(self):
        t1 = XArray([1, 2, 3])
        t2 = XArray([1, 0])
        with self.assertRaises(IndexError):
            _ = t1[t2]


class TestXArrayCopyRange(unittest.TestCase):
    """ 
    Tests XArray integer and range indexing
    """
    def test_copy_range_pos(self):
        t = XArray([1, 2, 3])
        self.assertEqual(1, t[0])

    def test_copy_range_neg(self):
        t = XArray([1, 2, 3])
        self.assertEqual(3, t[-1])

    def test_copy_range_index_err(self):
        t = XArray([1, 2, 3])
        with self.assertRaises(IndexError):
            _ = t[3]
        
    def test_copy_range_slice(self):
        t = XArray([1, 2, 3])
        res = t[0:2]
        self.assertEqual(2, len(res))
        self.assertEqual(1, res[0])
        self.assertEqual(2, res[1])

    def test_copy_range_slice_neg_start(self):
        t = XArray([1, 2, 3, 4, 5])
        res = t[-3:4]
        self.assertEqual(2, len(res))
        self.assertEqual(3, res[0])
        self.assertEqual(4, res[1])

    def test_copy_range_slice_neg_stop(self):
        t = XArray([1, 2, 3, 4, 5])
        res = t[1:-2]
        self.assertEqual(2, len(res))
        self.assertEqual(2, res[0])
        self.assertEqual(3, res[1])

    def test_copy_range_slice_stride(self):
        t = XArray([1, 2, 3, 4, 5])
        res = t[0:4:2]
        self.assertEqual(2, len(res))
        self.assertEqual(1, res[0])
        self.assertEqual(3, res[1])

    def test_copy_range_bad_type(self):
        t = XArray([1, 2, 3])
        with self.assertRaises(IndexError):
            _ = t[{1, 2, 3}]


class TestXArraySize(unittest.TestCase):
    """ 
    Tests XArray size operation
    """
    def test_size(self):
        t = XArray([1, 2, 3])
        self.assertEqual(3, t.size())


class TestXArrayDtype(unittest.TestCase):
    """ 
    Tests XArray dtype operation
    """
    def test_dtype(self):
        t = XArray([1, 2, 3])
        self.assertEqual(int, t.dtype())


class TestXArrayHead(unittest.TestCase):
    """ 
    Tests XArray head operation
    """
    def test_head(self):
        t = XArray([1, 2, 3])
        self.assertEqual(3, len(t.head()))

    def test_head_10(self):
        t = XArray(range(100))
        self.assertEqual(10, len(t.head()))

    def test_head_5(self):
        t = XArray(range(100))
        self.assertEqual(5, len(t.head(5)))


class TestXArrayVectorSlice(unittest.TestCase):
    """ 
    Tests XArray vector_slice operation
    """
    def test_vector_slice_start_0(self):
        t = XArray([[1, 2, 3], [10, 11, 12]])
        res = t.vector_slice(0)
        self.assertEqual(2, len(res))
        self.assertEqual(1, res[0])
        self.assertEqual(10, res[1])

    def test_vector_slice_start_1(self):
        t = XArray([[1, 2, 3], [10, 11, 12]])
        res = t.vector_slice(1)
        self.assertEqual(2, len(res))
        self.assertEqual(2, res[0])
        self.assertEqual(11, res[1])

    def test_vector_slice_start_end(self):
        t = XArray([[1, 2, 3], [10, 11, 12]])
        res = t.vector_slice(0, 2)
        self.assertEqual(2, len(res))
        self.assertTrue([1, 2], res[0])
        self.assertTrue([10, 11], res[1])

    def test_vector_slice_start_none(self):
        t = XArray([[1], [1, 2], [1, 2, 3]])
        res = t.vector_slice(2)
        self.assertEqual(3, len(res))
        self.assertEqual(None, res[0])
        self.assertEqual(None, res[1])
        self.assertEqual(3, res[2])

    def test_vector_slice_start_end_none(self):
        t = XArray([[1], [1, 2], [1, 2, 3]])
        res = t.vector_slice(0, 2)
        self.assertEqual(3, len(res))
        self.assertEqual(None, res[0])
        self.assertTrue([1, 2], res[1])
        self.assertTrue([1, 2], res[2])


class TestXArrayCountWords(unittest.TestCase):
    """ 
    Tests XArray count_words
    """
    def test_count_words(self):
        pass


class TestXArrayCountNgrams(unittest.TestCase):
    """ 
    Tests XArray count_ngrams
    """
    def test_count_ngrams(self):
        pass


class TestXArrayApply(unittest.TestCase):
    """ 
    Tests XArray apply
    """
    def test_apply_int(self):
        t = XArray([1, 2, 3])
        res = t.apply(lambda x: x * 2)
        self.assertEqual(3, len(res))
        self.assertEqual(int, res.dtype())
        self.assertEqual(2, res[0])
        self.assertEqual(4, res[1])
        self.assertEqual(6, res[2])

    def test_apply_float_cast(self):
        t = XArray([1, 2, 3])
        res = t.apply(lambda x: x * 2, float)
        self.assertEqual(3, len(res))
        self.assertEqual(float, res.dtype())
        self.assertEqual(2.0, res[0])
        self.assertEqual(4.0, res[1])
        self.assertEqual(6.0, res[2])

    def test_apply_skip_undefined(self):
        t = XArray([1, 2, 3, None])
        res = t.apply(lambda x: x * 2)
        self.assertEqual(4, len(res))
        self.assertEqual(int, res.dtype())
        self.assertEqual(2, res[0])
        self.assertEqual(4, res[1])
        self.assertEqual(6, res[2])
        self.assertEqual(None, res[3])

    def test_apply_type_err(self):
        t = XArray([1, 2, 3, None])
        with self.assertRaises(ValueError):
            t.apply(lambda x: x * 2, skip_undefined=False)

    def test_apply_fun_err(self):
        t = XArray([1, 2, 3, None])
        with self.assertRaises(TypeError):
            t.apply(1)


class TestXArrayFlatMap(unittest.TestCase):
    """ 
    Tests XArray flat_map
    """
    def test_flat_map(self):
        t = XArray([[1], [1, 2], [1, 2, 3]])
        res = t.flat_map(lambda x: x)
        self.assertEqual(6, len(res))
        self.assertEqual(int, res.dtype())
        self.assertEqual(1, res[0])
        self.assertEqual(1, res[1])
        self.assertEqual(2, res[2])
        self.assertEqual(1, res[3])
        self.assertEqual(2, res[4])
        self.assertEqual(3, res[5])

    def test_flat_map_int(self):
        t = XArray([[1], [1, 2], [1, 2, 3]])
        res = t.flat_map(lambda x: [v * 2 for v in x])
        self.assertEqual(6, len(res))
        self.assertEqual(int, res.dtype())
        self.assertEqual(2, res[0])
        self.assertEqual(2, res[1])
        self.assertEqual(4, res[2])
        self.assertEqual(2, res[3])
        self.assertEqual(4, res[4])
        self.assertEqual(6, res[5])

    def test_flat_map_str(self):
        t = XArray([['a'], ['a', 'b'], ['a', 'b', 'c']])
        res = t.flat_map(lambda x: x)
        self.assertEqual(6, len(res))
        self.assertEqual(str, res.dtype())
        self.assertEqual('a', res[0])
        self.assertEqual('a', res[1])
        self.assertEqual('b', res[2])
        self.assertEqual('a', res[3])
        self.assertEqual('b', res[4])
        self.assertEqual('c', res[5])

    def test_flat_map_float_cast(self):
        t = XArray([[1], [1, 2], [1, 2, 3]])
        res = t.flat_map(lambda x: x, dtype=float)
        self.assertEqual(6, len(res))
        self.assertEqual(float, res.dtype())
        self.assertEqual(1.0, res[0])
        self.assertEqual(1.0, res[1])
        self.assertEqual(2.0, res[2])
        self.assertEqual(1.0, res[3])
        self.assertEqual(2.0, res[4])
        self.assertEqual(3.0, res[5])

    def test_flat_map_skip_undefined(self):
        t = XArray([[1], [1, 2], [1, 2, 3], None, [None]])
        res = t.flat_map(lambda x: x)
        self.assertEqual(6, len(res))
        self.assertEqual(int, res.dtype())
        self.assertEqual(1, res[0])
        self.assertEqual(1, res[1])
        self.assertEqual(2, res[2])
        self.assertEqual(1, res[3])
        self.assertEqual(2, res[4])
        self.assertEqual(3, res[5])

    def test_flat_map_no_fun(self):
        t = XArray([[1], [1, 2], [1, 2, 3]])
        res = t.flat_map()
        self.assertEqual(6, len(res))
        self.assertEqual(int, res.dtype())
        self.assertEqual(1, res[0])
        self.assertEqual(1, res[1])
        self.assertEqual(2, res[2])
        self.assertEqual(1, res[3])
        self.assertEqual(2, res[4])
        self.assertEqual(3, res[5])

    def test_flat_map_type_err(self):
        t = XArray([[1], [1, 2], [1, 2, 3], [None]])
        with self.assertRaises(ValueError):
            t.flat_map(lambda x: x * 2, skip_undefined=False)


class TestXArrayFilter(unittest.TestCase):
    """ 
    Tests XArray filter
    """
    def test_filter(self):
        pass


class TestXArraySample(unittest.TestCase):
    """ 
    Tests XArray sample
    """
    def test_sample_no_seed(self):
        t = XArray(range(10))
        res = t.sample(0.3)
        self.assertTrue(len(res) < 10)

    @unittest.skip('depends on number of partitions')
    def test_sample_seed(self):
        t = XArray(range(10))
        res = t.sample(0.3, seed=1)
        # get 3, 6, 9 with this seed
        self.assertEqual(3, len(res))
        self.assertEqual(3, res[0])
        self.assertEqual(6, res[1])
        
    def test_sample_zero(self):
        t = XArray(range(10))
        res = t.sample(0.0)
        self.assertEqual(0, len(res))

    def test_sample_err_gt(self):
        t = XArray(range(10))
        with self.assertRaises(ValueError):
            t.sample(2, seed=1)

    def test_sample_err_lt(self):
        t = XArray(range(10))
        with self.assertRaises(ValueError):
            t.sample(-0.5, seed=1)


class TestXArraySaveAsText(unittest.TestCase):
    """ 
    Tests XArray save_as_text
    """
    def test_save_as_text(self):
        pass


class TestXArrayAll(unittest.TestCase):
    """ 
    Tests XArray all
    """
    # int
    def test_all_int_none(self):
        t = XArray([1, None])
        self.assertFalse(t.all())

    def test_all_int_zero(self):
        t = XArray([1, 0])
        self.assertFalse(t.all())

    def test_all_int_true(self):
        t = XArray([1, 2])
        self.assertTrue(t.all())

    # float
    def test_all_float_nan(self):
        t = XArray([1.0, float('nan')])
        self.assertFalse(t.all())

    def test_all_float_zero(self):
        t = XArray([1.0, 0.0])
        self.assertFalse(t.all())

    def test_all_float_true(self):
        t = XArray([1.0, 2.0])
        self.assertTrue(t.all())

    # str
    def test_all_str_empty(self):
        t = XArray(['hello', ''])
        self.assertFalse(t.all())

    def test_all_str_none(self):
        t = XArray(['hello', None])
        self.assertFalse(t.all())

    def test_all_str_true(self):
        t = XArray(['hello', 'world'])
        self.assertTrue(t.all())

    # list
    def test_all_list_empty(self):
        t = XArray([[1, 2], []])
        self.assertFalse(t.all())

    def test_all_list_none(self):
        t = XArray([[1, 2], None])
        self.assertFalse(t.all())

    def test_all_list_true(self):
        t = XArray([[1, 2], [2, 3]])
        self.assertTrue(t.all())

    # dict
    def test_all_dict_empty(self):
        t = XArray([{1: 'a'}, {}])
        self.assertFalse(t.all())

    def test_all_dict_none(self):
        t = XArray([{1: 'a'}, None])
        self.assertFalse(t.all())

    def test_all_dict_true(self):
        t = XArray([{1: 'a'}, {2: 'b'}])
        self.assertTrue(t.all())

    # empty
    def test_all_empty(self):
        t = XArray([])
        self.assertTrue(t.all())


class TestXArrayAny(unittest.TestCase):
    """ 
    Tests XArray any
    """
    # int
    def test_any_int(self):
        t = XArray([1, 2])
        self.assertTrue(t.any())

    def test_any_int_true(self):
        t = XArray([0, 1])
        self.assertTrue(t.any())

    def test_any_int_false(self):
        t = XArray([0, 0])
        self.assertFalse(t.any())

    def test_any_int_missing_true(self):
        t = XArray([1, None])
        self.assertTrue(t.any())

    def test_any_int_missing_false(self):
        t = XArray([None, 0])
        self.assertFalse(t.any())

    # float
    def test_any_float(self):
        t = XArray([1., 2.])
        self.assertTrue(t.any())

    def test_any_float_true(self):
        t = XArray([0.0, 1.0])
        self.assertTrue(t.any())

    def test_any_float_false(self):
        t = XArray([0.0, 0.0])
        self.assertFalse(t.any())

    def test_any_float_missing_true(self):
        t = XArray([1.0, None])
        self.assertTrue(t.any())

    def test_any_float_missing_true_nan(self):
        t = XArray([1.0, float('nan')])
        self.assertTrue(t.any())

    def test_any_float_missing_false(self):
        t = XArray([None, 0.0])
        self.assertFalse(t.any())

    def test_any_float_missing_false_nan(self):
        t = XArray([float('nan'), 0.0])
        self.assertFalse(t.any())

    # str
    def test_any_str(self):
        t = XArray(['a', 'b'])
        self.assertTrue(t.any())

    def test_any_str_true(self):
        t = XArray(['', 'a'])
        self.assertTrue(t.any())

    def test_any_str_false(self):
        t = XArray(['', ''])
        self.assertFalse(t.any())

    def test_any_str_missing_true(self):
        t = XArray(['a', None])
        self.assertTrue(t.any())

    def test_any_str_missing_false(self):
        t = XArray([None, ''])
        self.assertFalse(t.any())

    # list
    def test_any_list(self):
        t = XArray([[1], [2]])
        self.assertTrue(t.any())

    def test_any_list_true(self):
        t = XArray([[], ['a']])
        self.assertTrue(t.any())

    def test_any_list_false(self):
        t = XArray([[], []])
        self.assertFalse(t.any())

    def test_any_list_missing_true(self):
        t = XArray([['a'], None])
        self.assertTrue(t.any())

    def test_any_list_missing_false(self):
        t = XArray([None, []])
        self.assertFalse(t.any())

    # dict
    def test_any_dict(self):
        t = XArray([{'a': 1, 'b': 2}])
        self.assertTrue(t.any())

    def test_any_dict_true(self):
        t = XArray([{}, {'a': 1}])
        self.assertTrue(t.any())

    def test_any_dict_false(self):
        t = XArray([{}, {}])
        self.assertFalse(t.any())

    def test_any_dict_missing_true(self):
        t = XArray([{'a': 1}, None])
        self.assertTrue(t.any())

    def test_any_dict_missing_false(self):
        t = XArray([None, {}])
        self.assertFalse(t.any())

    # empty
    def test_any_empty(self):
        t = XArray([])
        self.assertFalse(t.any())


class TestXArrayMax(unittest.TestCase):
    """ 
    Tests XArray max
    """
    def test_max_empty(self):
        t = XArray([])
        self.assertEqual(None, t.max())

    def test_max_err(self):
        t = XArray(['a'])
        with self.assertRaises(TypeError):
            t.max()

    def test_max_int(self):
        t = XArray([1, 2, 3])
        self.assertEqual(3, t.max())

    def test_max_float(self):
        t = XArray([1.0, 2.0, 3.0])
        self.assertEqual(3.0, t.max())


class TestXArrayMin(unittest.TestCase):
    """ 
    Tests XArray min
    """
    def test_min_empty(self):
        t = XArray([])
        self.assertEqual(None, t.min())

    def test_min_err(self):
        t = XArray(['a'])
        with self.assertRaises(TypeError):
            t.min()

    def test_min_int(self):
        t = XArray([1, 2, 3])
        self.assertEqual(1, t.min())

    def test_min_float(self):
        t = XArray([1.0, 2.0, 3.0])
        self.assertEqual(1.0, t.min())


class TestXArraySum(unittest.TestCase):
    """ 
    Tests XArray sum
    """
    def test_sum_empty(self):
        t = XArray([])
        self.assertEqual(None, t.sum())

    def test_sum_err(self):
        t = XArray(['a'])
        with self.assertRaises(TypeError):
            t.sum()

    def test_sum_int(self):
        t = XArray([1, 2, 3])
        self.assertEqual(6, t.sum())

    def test_sum_float(self):
        t = XArray([1.0, 2.0, 3.0])
        self.assertEqual(6.0, t.sum())


class TestXArrayMean(unittest.TestCase):
    """ 
    Tests XArray mean
    """
    def test_mean_empty(self):
        t = XArray([])
        self.assertEqual(None, t.mean())

    def test_mean_err(self):
        t = XArray(['a'])
        with self.assertRaises(TypeError):
            t.mean()

    def test_mean_int(self):
        t = XArray([1, 2, 3])
        self.assertEqual(2, t.mean())

    def test_mean_float(self):
        t = XArray([1.0, 2.0, 3.0])
        self.assertEqual(2.0, t.mean())


class TestXArrayStd(unittest.TestCase):
    """ 
    Tests XArray std
    """
    def test_std_empty(self):
        t = XArray([])
        self.assertEqual(None, t.std())

    def test_std_err(self):
        t = XArray(['a'])
        with self.assertRaises(TypeError):
            t.std()

    def test_std_int(self):
        t = XArray([1, 2, 3])
        expect = math.sqrt(2.0 / 3.0)
        self.assertEqual(expect, t.std())

    def test_std_float(self):
        t = XArray([1.0, 2.0, 3.0])
        expect = math.sqrt(2.0 / 3.0)
        self.assertEqual(expect, t.std())


class TestXArrayVar(unittest.TestCase):
    """ 
    Tests XArray var
    """
    def test_var_empty(self):
        t = XArray([])
        self.assertEqual(None, t.var())

    def test_var_err(self):
        t = XArray(['a'])
        with self.assertRaises(TypeError):
            t.var()

    def test_var_int(self):
        t = XArray([1, 2, 3])
        expect = 2.0 / 3.0
        self.assertEqual(expect, t.var())

    def test_var_float(self):
        t = XArray([1.0, 2.0, 3.0])
        expect = 2.0 / 3.0
        self.assertEqual(expect, t.var())


class TestXArrayNumMissing(unittest.TestCase):
    """ 
    Tests XArray num_missing
    """
    def test_num_missing_empty(self):
        t = XArray([])
        self.assertEqual(0, t.num_missing())

    def test_num_missing_zero(self):
        t = XArray([1, 2, 3])
        self.assertEqual(0, t.num_missing())

    def test_num_missing_int_none(self):
        t = XArray([1, 2, None])
        self.assertEqual(1, t.num_missing())

    def test_num_missing_int_all(self):
        t = XArray([None, None, None], dtype=int)
        self.assertEqual(3, t.num_missing())

    def test_num_missing_float_none(self):
        t = XArray([1.0, 2.0, None])
        self.assertEqual(1, t.num_missing())

    def test_num_missing_float_nan(self):
        t = XArray([1.0, 2.0, float('nan')])
        self.assertEqual(1, t.num_missing())


class TestXArrayNumNonzero(unittest.TestCase):
    """ 
    Tests XArray nnz
    """
    def test_nnz_empty(self):
        t = XArray([])
        self.assertEqual(0, t.nnz())

    def test_nnz_zero_int(self):
        t = XArray([0, 0, 0])
        self.assertEqual(0, t.nnz())

    def test_nnz_zero_float(self):
        t = XArray([0.0, 0.0, 0.0])
        self.assertEqual(0, t.nnz())

    def test_nnz_int_none(self):
        t = XArray([1, 2, None])
        self.assertEqual(2, t.nnz())

    def test_nnz_int_all(self):
        t = XArray([None, None, None], dtype=int)
        self.assertEqual(0, t.nnz())

    def test_nnz_float_none(self):
        t = XArray([1.0, 2.0, None])
        self.assertEqual(2, t.nnz())

    def test_nnz_float_nan(self):
        t = XArray([1.0, 2.0, float('nan')])
        self.assertEqual(2, t.nnz())


class TestXArrayDatetimeToStr(unittest.TestCase):
    """ 
    Tests XArray datetime_to_str
    """
    def test_datetime_to_str(self):
        pass


class TestXArrayStrToDatetime(unittest.TestCase):
    """ 
    Tests XArray str_to_datetime
    """
    def test_str_to_datetime(self):
        pass


class TestXArrayAstype(unittest.TestCase):
    """ 
    Tests XArray astype
    """
    def test_astype_empty(self):
        t = XArray([])
        res = t.astype(int)
        self.assertEqual(int, res.dtype())

    def test_astype_int_int(self):
        t = XArray([1, 2, 3])
        res = t.astype(int)
        self.assertEqual(int, res.dtype())
        self.assertEqual(1, res[0])

    def test_astype_int_float(self):
        t = XArray([1, 2, 3])
        res = t.astype(float)
        self.assertEqual(float, res.dtype())
        self.assertEqual(1.0, res[0])

    def test_astype_float_float(self):
        t = XArray([1.0, 2.0, 3.0])
        res = t.astype(float)
        self.assertEqual(float, res.dtype())
        self.assertEqual(1.0, res[0])

    def test_astype_float_int(self):
        t = XArray([1.0, 2.0, 3.0])
        res = t.astype(int)
        self.assertEqual(int, res.dtype())
        self.assertEqual(1, res[0])

    def test_astype_int_str(self):
        t = XArray([1, 2, 3])
        res = t.astype(str)
        self.assertEqual(str, res.dtype())
        self.assertEqual('1', res[0])

    def test_astype_str_list(self):
        t = XArray(['[1, 2, 3]', '[4, 5, 6]'])
        res = t.astype(list)
        self.assertEqual(list, res.dtype())
        self.assertTrue([1, 2, 3], res[0])

    def test_astype_str_dict(self):
        t = XArray(['{"a": 1, "b": 2}', '{"x": 3}'])
        res = t.astype(dict)
        self.assertEqual(dict, res.dtype())
        self.assertEqual({'a': 1, 'b': 2}, res[0])


class TestXArrayClip(unittest.TestCase):
    """ 
    Tests XArray clip
    """
    def test_clip_int_nan(self):
        nan = float('nan')
        t = XArray([1, 2, 3])
        res = t.clip(nan, nan)
        self.assertTrue(eq_list([1, 2, 3], res))

    def test_clip_int_def(self):
        t = XArray([1, 2, 3])
        res = t.clip()
        self.assertTrue(eq_list([1, 2, 3], res))

    def test_clip_float_nan(self):
        nan = float('nan')
        t = XArray([1.0, 2.0, 3.0])
        res = t.clip(nan, nan)
        self.assertTrue(eq_list([1.0, 2.0, 3.0], res))

    def test_clip_float_def(self):
        t = XArray([1.0, 2.0, 3.0])
        res = t.clip()
        self.assertTrue(eq_list([1.0, 2.0, 3.0], res))

    def test_clip_int_all(self):
        t = XArray([1, 2, 3])
        res = t.clip(1, 3)
        self.assertTrue(eq_list([1, 2, 3], res))

    def test_clip_float_all(self):
        t = XArray([1.0, 2.0, 3.0])
        res = t.clip(1.0, 3.0)
        self.assertTrue(eq_list([1.0, 2.0, 3.0], res))

    def test_clip_int_clip(self):
        t = XArray([1, 2, 3])
        res = t.clip(2, 2)
        self.assertTrue(eq_list([2, 2, 2], res))

    def test_clip_float_clip(self):
        t = XArray([1.0, 2.0, 3.0])
        res = t.clip(2.0, 2.0)
        self.assertTrue(eq_list([2.0, 2.0, 2.0], res))

    def test_clip_list_nan(self):
        nan = float('nan')
        t = XArray([[1, 2, 3]])
        res = t.clip(nan, nan)
        self.assertTrue(eq_list([[1, 2, 3]], res))

    def test_clip_list_def(self):
        t = XArray([[1, 2, 3]])
        res = t.clip()
        self.assertTrue(eq_list([[1, 2, 3]], res))

    def test_clip_list_all(self):
        t = XArray([[1, 2, 3]])
        res = t.clip(1, 3)
        self.assertTrue(eq_list([[1, 2, 3]], res))

    def test_clip_list_clip(self):
        t = XArray([[1, 2, 3]])
        res = t.clip(2, 2)
        self.assertTrue(eq_list([[2, 2, 2]], res))


class TestXArrayClipLower(unittest.TestCase):
    """ 
    Tests XArray clip_lower
    """
    def test_clip_lower_int_all(self):
        t = XArray([1, 2, 3])
        res = t.clip_lower(1)
        self.assertTrue(eq_list([1, 2, 3], res))

    def test_clip_int_clip(self):
        t = XArray([1, 2, 3])
        res = t.clip_lower(2)
        self.assertTrue(eq_list([2, 2, 3], res))

    def test_clip_lower_list_all(self):
        t = XArray([[1, 2, 3]])
        res = t.clip_lower(1)
        self.assertTrue(eq_list([[1, 2, 3]], res))

    def test_clip_lower_list_clip(self):
        t = XArray([[1, 2, 3]])
        res = t.clip_lower(2)
        self.assertTrue(eq_list([[2, 2, 3]], res))


class TestXArrayClipUpper(unittest.TestCase):
    """ 
    Tests XArray clip_upper
    """
    def test_clip_upper_int_all(self):
        t = XArray([1, 2, 3])
        res = t.clip_upper(3)
        self.assertTrue(eq_list([1, 2, 3], res))

    def test_clip_int_clip(self):
        t = XArray([1, 2, 3])
        res = t.clip_upper(2)
        self.assertTrue(eq_list([1, 2, 2], res))

    def test_clip_upper_list_all(self):
        t = XArray([[1, 2, 3]])
        res = t.clip_upper(3)
        self.assertTrue(eq_list([[1, 2, 3]], res))

    def test_clip_upper_list_clip(self):
        t = XArray([[1, 2, 3]])
        res = t.clip_upper(2)
        self.assertTrue(eq_list([[1, 2, 2]], res))


class TestXArrayTail(unittest.TestCase):
    """ 
    Tests XArray tail
    """
    def test_tail(self):
        t = XArray(range(1, 100))
        res = t.tail(10)
        self.assertEqual(range(90, 100), res)

    def test_tail_all(self):
        t = XArray(range(1, 100))
        res = t.tail(100)
        self.assertEqual(range(1, 100), res)


class TestXArrayDropna(unittest.TestCase):
    """ 
    Tests XArray dropna
    """
    def test_dropna_not(self):
        t = XArray([1, 2, 3])
        res = t.dropna()
        self.assertTrue(eq_list([1, 2, 3], res))

    def test_dropna_none(self):
        t = XArray([1, 2, None])
        res = t.dropna()
        self.assertTrue(eq_list([1, 2], res))

    def test_dropna_nan(self):
        t = XArray([1.0, 2.0, float('nan')])
        res = t.dropna()
        self.assertTrue(eq_list([1.0, 2.0], res))


class TestXArrayFillna(unittest.TestCase):
    """ 
    Tests XArray fillna
    """
    def test_fillna_not(self):
        t = XArray([1, 2, 3])
        res = t.fillna(10)
        self.assertTrue(eq_list([1, 2, 3], res))

    def test_fillna_none(self):
        t = XArray([1, 2, None])
        res = t.fillna(10)
        self.assertTrue(eq_list([1, 2, 10], res))

    def test_fillna_none_cast(self):
        t = XArray([1, 2, None])
        res = t.fillna(10.0)
        self.assertTrue(eq_list([1, 2, 10], res))

    def test_fillna_nan(self):
        t = XArray([1.0, 2.0, float('nan')])
        res = t.fillna(10.0)
        self.assertTrue(eq_list([1.0, 2.0, 10.0], res))

    def test_fillna_nan_cast(self):
        t = XArray([1.0, 2.0, float('nan')])
        res = t.fillna(10)
        self.assertTrue(eq_list([1.0, 2.0, 10.0], res))


class TestXArrayTopkIndex(unittest.TestCase):
    """ 
    Tests XArray topk_index
    """
    def test_topk_index_0(self):
        t = XArray([1, 2, 3])
        res = t.topk_index(0)
        self.assertTrue(eq_list([0, 0, 0], res))

    def test_topk_index_1(self):
        t = XArray([1, 2, 3])
        res = t.topk_index(1)
        self.assertTrue(eq_list([0, 0, 1], res))

    def test_topk_index_2(self):
        t = XArray([1, 2, 3])
        res = t.topk_index(2)
        self.assertTrue(eq_list([0, 1, 1], res))

    def test_topk_index_3(self):
        t = XArray([1, 2, 3])
        res = t.topk_index(3)
        self.assertTrue(eq_list([1, 1, 1], res))

    def test_topk_index_4(self):
        t = XArray([1, 2, 3])
        res = t.topk_index(4)
        self.assertTrue(eq_list([1, 1, 1], res))

    def test_topk_index_float_1(self):
        t = XArray([1.0, 2.0, 3.0])
        res = t.topk_index(1)
        self.assertTrue(eq_list([0, 0, 1], res))

    def test_topk_index_str_1(self):
        t = XArray(['a', 'b', 'c'])
        res = t.topk_index(1)
        self.assertTrue(eq_list([0, 0, 1], res))

    def test_topk_index_list_1(self):
        t = XArray([[1, 2, 3], [2, 3, 4], [3, 4, 5]])
        res = t.topk_index(1)
        self.assertTrue(eq_list([0, 0, 1], res))

    def test_topk_index_reverse_int(self):
        t = XArray([1, 2, 3])
        res = t.topk_index(1, reverse=True)
        self.assertTrue(eq_list([1, 0, 0], res))

    def test_topk_index_reverse_float(self):
        t = XArray([1.0, 2.0, 3.0])
        res = t.topk_index(1, reverse=True)
        self.assertTrue(eq_list([1, 0, 0], res))

    def test_topk_index_reverse_str(self):
        t = XArray(['a', 'b', 'c'])
        res = t.topk_index(1, reverse=True)
        self.assertTrue(eq_list([1, 0, 0], res))

    def test_topk_index_reverse_list(self):
        t = XArray([[1, 2, 3], [2, 3, 4], [3, 4, 5]])
        res = t.topk_index(1, reverse=True)
        self.assertTrue(eq_list([1, 0, 0], res))


class TestXArraySketchSummary(unittest.TestCase):
    """ 
    Tests XArray sketch_summary
    """
    def test_sketch_summary_size(self):
        t = XArray([1, 2, 3, 4, 5])
        ss = t.sketch_summary()
        self.assertEqual(5, ss.size())

    def test_sketch_summary_min(self):
        t = XArray([1, 2, 3, 4, 5])
        ss = t.sketch_summary()
        self.assertEqual(1, ss.min())

    def test_sketch_summary_max(self):
        t = XArray([1, 2, 3, 4, 5])
        ss = t.sketch_summary()
        self.assertEqual(5, ss.max())

    def test_sketch_summary_mean(self):
        t = XArray([1, 2, 3, 4, 5])
        ss = t.sketch_summary()
        self.assertEqual(3.0, ss.mean())

    def test_sketch_summary_sum(self):
        t = XArray([1, 2, 3, 4, 5])
        ss = t.sketch_summary()
        self.assertEqual(15, ss.sum())

    def test_sketch_summary_var(self):
        t = XArray([1, 2, 3, 4, 5])
        ss = t.sketch_summary()
        self.assertEqual(2.0, ss.var())

    def test_sketch_summary_std(self):
        t = XArray([1, 2, 3, 4, 5])
        ss = t.sketch_summary()
        self.assertEqual(math.sqrt(2.0), ss.std())

    def test_sketch_summary_num_undefined(self):
        t = XArray([1, None, 3, None, 5])
        ss = t.sketch_summary()
        self.assertEqual(2, ss.num_undefined())

    def test_sketch_summary_num_unique(self):
        t = XArray([1, 3, 3, 3, 5])
        ss = t.sketch_summary()
        self.assertEqual(3, ss.num_unique())

    # TODO files on multiple workers
    # probably something wrong with combiner
    def test_sketch_summary_frequent_items(self):
        t = XArray([1, 3, 3, 3, 5])
        ss = t.sketch_summary()
        self.assertEqual({1: 1, 3: 3, 5: 1}, ss.frequent_items())

    def test_sketch_summary_frequency_count(self):
        t = XArray([1, 3, 3, 3, 5])
        ss = t.sketch_summary()
        self.assertEqual(1, ss.frequency_count(1))
        self.assertEqual(3, ss.frequency_count(3))
        self.assertEqual(1, ss.frequency_count(5))


class TestXArrayAppend(unittest.TestCase):
    """ 
    Tests XArray append
    """
    def test_append(self):
        t = XArray([1, 2, 3])
        u = XArray([10, 20, 30])
        res = t.append(u)
        self.assertTrue(eq_list([1, 2, 3, 10, 20, 30], res))

    def test_append_empty_t(self):
        t = XArray([], dtype=int)
        u = XArray([10, 20, 30])
        res = t.append(u)
        self.assertTrue(eq_list([10, 20, 30], res))

    def test_append_empty_u(self):
        t = XArray([1, 2, 3])
        u = XArray([], dtype=int)
        res = t.append(u)
        self.assertTrue(eq_list([1, 2, 3], res))

    def test_append_int_float_err(self):
        t = XArray([1, 2, 3])
        u = XArray([10., 20., 30.])
        with self.assertRaises(RuntimeError):
            t.append(u)

    def test_append_int_str_err(self):
        t = XArray([1, 2, 3])
        u = XArray(['a', 'b', 'c'])
        with self.assertRaises(RuntimeError):
            t.append(u)


class TestXArrayUnique(unittest.TestCase):
    """ 
    Tests XArray unique
    """
    def test_unique_dict_err(self):
        t = XArray([{'a': 1, 'b': 2, 'c': 3}])
        with self.assertRaises(TypeError):
            t.unique()

    def test_unique_int_noop(self):
        t = XArray([1, 2, 3])
        res = t.unique()
        self.assertEquals(3, len(res))
        self.assertTrue(eq_list([1, 2, 3], sorted(list(res))))

    def test_unique_float_noop(self):
        t = XArray([1.0, 2.0, 3.0])
        res = t.unique()
        self.assertEquals(3, len(res))
        self.assertTrue(eq_list([1.0, 2.0, 3.0], sorted(list(res))))

    def test_unique_str_noop(self):
        t = XArray(['1', '2', '3'])
        res = t.unique()
        self.assertEquals(3, len(res))
        self.assertTrue(eq_list(['1', '2', '3'], sorted(list(res))))

    def test_unique_int(self):
        t = XArray([1, 2, 3, 1, 2])
        res = t.unique()
        self.assertEquals(3, len(res))
        self.assertTrue(eq_list([1, 2, 3], sorted(list(res))))

    def test_unique_float(self):
        t = XArray([1.0, 2.0, 3.0, 1.0, 2.0])
        res = t.unique()
        self.assertEquals(3, len(res))
        self.assertTrue(eq_list([1.0, 2.0, 3.0], sorted(list(res))))

    def test_unique_str(self):
        t = XArray(['1', '2', '3', '1', '2'])
        res = t.unique()
        self.assertEquals(3, len(res))
        self.assertTrue(eq_list(['1', '2', '3'], sorted(list(res))))


class TestXArrayItemLength(unittest.TestCase):
    """ 
    Tests XArray item_length
    """
    def test_item_length_int(self):
        t = XArray([1, 2, 3])
        with self.assertRaises(TypeError):
            t.item_length()

    def test_item_length_float(self):
        t = XArray([1.0, 2.0, 3.0])
        with self.assertRaises(TypeError):
            t.item_length()

    def test_item_length_str(self):
        t = XArray(['a', 'bb', 'ccc'])
        res = t.item_length()
        self.assertTrue(eq_list([1, 2, 3], res))
        self.assertEqual(int, res.dtype())

    def test_item_length_list(self):
        t = XArray([[1], [1, 2], [1, 2, 3]])
        res = t.item_length()
        self.assertTrue(eq_list([1, 2, 3], res))
        self.assertEqual(int, res.dtype())

    def test_item_length_dict(self):
        t = XArray([{1: 'a'}, {1: 'a', 2: 'b'}, {1: 'a', 2: 'b', 3: '3'}])
        res = t.item_length()
        self.assertTrue(eq_list([1, 2, 3], res))
        self.assertEqual(int, res.dtype())


class TestXArrayUnpackErrors(unittest.TestCase):
    """ 
    Tests XArray unpack errors
    """
    def test_unpack_str(self):
        t = XArray(['a', 'b', 'c'])
        with self.assertRaises(TypeError):
            t.unpack()

    def test_unpack_bad_prefix(self):
        t = XArray([[1, 2, 3], [4, 5, 6]])
        with self.assertRaises(TypeError):
            t.unpack(column_name_prefix=1)

    def test_unpack_bad_limit_type(self):
        t = XArray([[1, 2, 3], [4, 5, 6]])
        with self.assertRaises(TypeError):
            t.unpack(limit=1)

    def test_unpack_bad_limit_val(self):
        t = XArray([[1, 2, 3], [4, 5, 6]])
        with self.assertRaises(TypeError):
            t.unpack(limit=['a', 1])

    def test_unpack_bad_limit_dup(self):
        t = XArray([[1, 2, 3], [4, 5, 6]])
        with self.assertRaises(ValueError):
            t.unpack(limit=[1, 1])

    def test_unpack_bad_column_types(self):
        t = XArray([[1, 2, 3], [4, 5, 6]])
        with self.assertRaises(TypeError):
            t.unpack(column_types=1)

    def test_unpack_bad_column_types_bool(self):
        t = XArray([[1, 2, 3], [4, 5, 6]])
        with self.assertRaises(TypeError):
            t.unpack(column_types=[True])

    def test_unpack_column_types_limit_mismatch(self):
        t = XArray([[1, 2, 3], [4, 5, 6]])
        with self.assertRaises(ValueError):
            t.unpack(limit=[1], column_types=[int, int])

    def test_unpack_dict_column_types_no_limit(self):
        t = XArray([{'a': 1, 'b': 2}, {'c': 3, 'd': 4}])
        with self.assertRaises(ValueError):
            t.unpack(column_types=[int, int])

    def test_unpack_empty_no_column_types(self):
        t = XArray([], dtype=list)
        with self.assertRaises(RuntimeError):
            t.unpack()

    def test_unpack_empty_list_column_types(self):
        t = XArray([[]], dtype=list)
        with self.assertRaises(RuntimeError):
            t.unpack()


class TestXArrayUnpack(unittest.TestCase):
    """ 
    Tests XArray unpack list
    """
    def test_unpack_list(self):
        t = XArray([[1, 0, 1],
                    [1, 1, 1],
                    [0, 1]])
        res = t.unpack()
        self.assertEqual(['X.0', 'X.1', 'X.2'], res.column_names())
        self.assertTrue([1, 0, 1], res[0])
        self.assertTrue([1, 1, 1], res[1])
        self.assertTrue([0, 1, None], res[2])

    def test_unpack_list_limit(self):
        t = XArray([[1, 0, 1],
                    [1, 1, 1],
                    [0, 1]])
        res = t.unpack(limit=[1])
        self.assertEqual(['X.1'], res.column_names())
        self.assertTrue([0], res[0])
        self.assertTrue([1], res[1])
        self.assertTrue([1], res[2])

    def test_unpack_list_na_values(self):
        t = XArray([[1, 0, 1],
                    [1, 1, 1],
                    [0, 1]])
        res = t.unpack(na_value=0)
        self.assertEqual(['X.0', 'X.1', 'X.2'], res.column_names())
        self.assertTrue([1, 0, 1], res[0])
        self.assertTrue([1, 1, 1], res[1])
        self.assertTrue([0, 1, 0], res[2])

    def test_unpack_list_na_values_col_types(self):
        t = XArray([[1, 0, 1],
                    [1, 1, 1],
                    [0, 1]])
        res = t.unpack(column_types=[int, int, int], na_value=0)
        self.assertEqual(['X.0', 'X.1', 'X.2'], res.column_names())
        self.assertTrue([1, 0, 1], res[0])
        self.assertTrue([1, 1, 1], res[1])
        self.assertTrue([0, 1, 0], res[2])

    def test_unpack_list_cast_str(self):
        t = XArray([[1, 0, 1],
                    [1, 1, 1],
                    [0, 1]])
        res = t.unpack(column_types=[str, str, str])
        self.assertEqual(['X.0', 'X.1', 'X.2'], res.column_names())
        self.assertTrue(['1', '0', '1'], res[0])
        self.assertTrue(['1', '1', '1'], res[1])
        self.assertTrue(['0', '1', None], res[2])

    def test_unpack_list_no_prefix(self):
        t = XArray([[1, 0, 1],
                    [1, 1, 1],
                    [0, 1]])
        res = t.unpack(column_name_prefix='')
        self.assertEqual(['0', '1', '2'], res.column_names())
        self.assertTrue([1, 0, 1], res[0])
        self.assertTrue([1, 1, 1], res[1])
        self.assertTrue([0, 1, None], res[2])

    def test_unpack_dict_limit(self):
        t = XArray([{'word': 'a', 'count': 1},
                    {'word': 'cat', 'count': 2},
                    {'word': 'is', 'count': 3},
                    {'word': 'coming', 'count': 4}])
        res = t.unpack(limit=['word', 'count'], column_types=[str, int])
        self.assertEqual(['X.word', 'X.count'], res.column_names())
        self.assertTrue(['a', 1], res[0])
        self.assertTrue(['cat', 2], res[1])
        self.assertTrue(['is', 3], res[2])
        self.assertTrue(['coming', 4], res[3])

    def test_unpack_dict_limit_word(self):
        t = XArray([{'word': 'a', 'count': 1},
                    {'word': 'cat', 'count': 2},
                    {'word': 'is', 'count': 3},
                    {'word': 'coming', 'count': 4}])
        res = t.unpack(limit=['word'])
        self.assertEqual(['X.word'], res.column_names())
        self.assertTrue(['a'], res[0])
        self.assertTrue(['cat'], res[1])
        self.assertTrue(['is'], res[2])
        self.assertTrue(['coming'], res[3])

    def test_unpack_dict_limit_count(self):
        t = XArray([{'word': 'a', 'count': 1},
                    {'word': 'cat', 'count': 2},
                    {'word': 'is', 'count': 3},
                    {'word': 'coming', 'count': 4}])
        res = t.unpack(limit=['count'])
        self.assertEqual(['X.count'], res.column_names())
        self.assertTrue([1], res[0])
        self.assertTrue([2], res[1])
        self.assertTrue([3], res[2])
        self.assertTrue([4], res[3])

    def test_unpack_dict_incomplete(self):
        t = XArray([{'word': 'a', 'count': 1},
                    {'word': 'cat', 'count': 2},
                    {'word': 'is'},
                    {'word': 'coming', 'count': 4}])
        res = t.unpack(limit=['word', 'count'], column_types=[str, int])
        self.assertEqual(['X.word', 'X.count'], res.column_names())
        self.assertTrue(['a', 1], res[0])
        self.assertTrue(['cat', 2], res[1])
        self.assertTrue(['is', None], res[2])
        self.assertTrue(['coming', 4], res[3])

    def test_unpack_dict(self):
        t = XArray([{'word': 'a', 'count': 1},
                    {'word': 'cat', 'count': 2},
                    {'word': 'is', 'count': 3},
                    {'word': 'coming', 'count': 4}])
        res = t.unpack()
        self.assertEqual(['X.count', 'X.word'], res.column_names())
        self.assertTrue([1, 'a'], res[0])
        self.assertTrue([2, 'cat'], res[1])
        self.assertTrue([3, 'is'], res[2])
        self.assertTrue([4, 'coming'], res[3])

    def test_unpack_dict_no_prefix(self):
        t = XArray([{'word': 'a', 'count': 1},
                    {'word': 'cat', 'count': 2},
                    {'word': 'is', 'count': 3},
                    {'word': 'coming', 'count': 4}])
        res = t.unpack(column_name_prefix=None)
        self.assertEqual(['count', 'word'], res.column_names())
        self.assertTrue([1, 'a'], res[0])
        self.assertTrue([2, 'cat'], res[1])
        self.assertTrue([3, 'is'], res[2])
        self.assertTrue([4, 'coming'], res[3])


class TestXArraySort(unittest.TestCase):
    """ 
    Tests XArray sort
    """
    def test_sort_int(self):
        t = XArray([3, 2, 1])
        res = t.sort()
        self.assertTrue(eq_list([1, 2, 3], res))

    def test_sort_float(self):
        t = XArray([3, 2, 1])
        res = t.sort()
        self.assertTrue(eq_list([1.0, 2.0, 3.0], res))

    def test_sort_str(self):
        t = XArray(['c', 'b', 'a'])
        res = t.sort()
        self.assertTrue(eq_list(['a', 'b', 'c'], res))

    def test_sort_list(self):
        t = XArray([[3, 4], [2, 3], [1, 2]])
        with self.assertRaises(TypeError):
            t.sort()

    def test_sort_dict(self):
        t = XArray([{'c': 3}, {'b': 2}, {'a': 1}])
        with self.assertRaises(TypeError):
            t.sort()

    def test_sort_int_desc(self):
        t = XArray([1, 2, 3])
        res = t.sort(ascending=False)
        self.assertTrue(eq_list([3, 2, 1], res))

    def test_sort_float_desc(self):
        t = XArray([1.0, 2.0, 3.0])
        res = t.sort(ascending=False)
        self.assertTrue(eq_list([3.0, 2.0, 1.0], res))

    def test_sort_str_desc(self):
        t = XArray(['a', 'b', 'c'])
        res = t.sort(ascending=False)
        self.assertTrue(eq_list(['c', 'b', 'a'], res))


class TestXArrayDictTrimByKeys(unittest.TestCase):
    """ 
    Tests XArray dict_trim_by_keys
    """
    def test_dict_trim_by_keys_bad_type(self):
        t = XArray([3, 2, 1])
        with self.assertRaises(TypeError):
            t.dict_trim_by_keys(['a'])

    def test_dict_trim_by_keys_include(self):
        t = XArray([{'a': 0, 'b': 0, 'c': 0}, {'x': 1}])
        res = t.dict_trim_by_keys(['a'], exclude=False)
        self.assertEqual([{'a': 0}, {}], res)

    def test_dict_trim_by_keys_exclude(self):
        t = XArray([{'a': 0, 'b': 0, 'c': 0}, {'x': 1}])
        res = t.dict_trim_by_keys(['a'])
        self.assertEqual([{'b': 1, 'c': 2}, {'x': 1}], res)


class TestXArrayDictTrimByValues(unittest.TestCase):
    """ 
    Tests XArray dict_trim_by_values
    """
    def test_dict_trim_by_values_bad_type(self):
        t = XArray([3, 2, 1])
        with self.assertRaises(TypeError):
            t.dict_trim_by_values(1, 2)

    def test_dict_trim_by_values(self):
        t = XArray([{'a': 0, 'b': 1, 'c': 2, 'd': 3}, {'x': 1}])
        res = t.dict_trim_by_values(1, 2)
        self.assertEqual([{'b': 1, 'c': 2}, {'x': 1}], res)


class TestXArrayDictKeys(unittest.TestCase):
    """ 
    Tests XArray dict_keys
    """
    # noinspection PyArgumentList
    def test_dict_keys_bad_type(self):
        t = XArray([3, 2, 1])
        with self.assertRaises(TypeError):
            t.dict_keys(['a'])

    def test_dict_keys_bad_len(self):
        t = XArray([{'a': 0, 'b': 0, 'c': 0}, {'x': 1}])
        with self.assertRaises(ValueError):
            t.dict_keys()

    def test_dict_keys(self):
        t = XArray([{'a': 0, 'b': 0, 'c': 0}, {'x': 1, 'y': 2, 'z': 3}])
        res = t.dict_keys()
        self.assertEqual(2, len(res))
        self.assertEqual({'X.0': 'a', 'X.1': 'c', 'X.2': 'b'}, res[0])
        self.assertEqual({'X.0': 'y', 'X.1': 'x', 'X.2': 'z'}, res[1])


class TestXArrayDictValues(unittest.TestCase):
    """ 
    Tests XArray dict_values
    """
    # noinspection PyArgumentList
    def test_values_bad_type(self):
        t = XArray([3, 2, 1])
        with self.assertRaises(TypeError):
            t.dict_values(['a'])

    def test_values_bad_len(self):
        t = XArray([{'a': 0, 'b': 1, 'c': 2}, {'x': 10}])
        with self.assertRaises(ValueError):
            t.dict_values()

    def test_values(self):
        t = XArray([{'a': 0, 'b': 1, 'c': 2}, {'x': 10, 'y': 20, 'z': 30}])
        res = t.dict_values()
        self.assertEqual(2, len(res))
        self.assertEqual({'X.0': 0, 'X.1': 2, 'X.2': 1}, res[0])
        self.assertEqual({'X.0': 20, 'X.1': 10, 'X.2': 30}, res[1])


class TestXArrayDictHasAnyKeys(unittest.TestCase):
    """ 
    Tests XArray dict_has_any_keys
    """
    def test_dict_has_any_keys_bad(self):
        t = XArray([3, 2, 1])
        with self.assertRaises(TypeError):
            t.dict_has_any_keys(['a'])

    def test_dict_has_any_keys(self):
        t = XArray([{'a': 0, 'b': 0, 'c': 0}, {'x': 1}])
        res = t.dict_has_any_keys(['a'])
        self.assertEqual([True, False], res)


class TestXArrayDictHasAllKeys(unittest.TestCase):
    """ 
    Tests XArray dict_has_all_keys
    """
    def test_dict_has_all_keys_bad(self):
        t = XArray([3, 2, 1])
        with self.assertRaises(TypeError):
            t.dict_has_all_keys(['a'])

    def test_dict_has_all_keys(self):
        t = XArray([{'a': 0, 'b': 0, 'c': 0}, {'a': 1, 'b': 1}])
        res = t.dict_has_all_keys(['a', 'b', 'c'])
        self.assertEqual([True, False], res)

if __name__ == '__main__':
    unittest.main()