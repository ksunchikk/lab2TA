import unittest
import RegExp

class test_exep(unittest.TestCase):
    def _compile_(self):
        self.reg = None
    def test1(self):
        with self.assertRaises(Exception) as context:
            RegExp.RegExp('(u|k)..')
        self.assertTrue('Syntax error!' in str(context.exception))
    def test2(self):
        with self.assertRaises(Exception) as context:
            RegExp.RegExp('(u||k)...')
        self.assertTrue('Syntax error!' in str(context.exception))
    def test3(self):
        with self.assertRaises(Exception) as context:
            RegExp.RegExp('(u|k)[]')
        self.assertTrue('Syntax error!' in str(context.exception))
    def test4(self):
        with self.assertRaises(Exception) as context:
            RegExp.RegExp('(u|k){8')
        self.assertTrue('Syntax error!' in str(context.exception))
    def test5(self):
        with self.assertRaises(Exception) as context:
            RegExp.RegExp('(u|k)[oi')
        self.assertTrue('Syntax error!' in str(context.exception))
    def test6(self):
        with self.assertRaises(Exception) as context:
            RegExp.RegExp('(u|k)8}}')
        self.assertTrue('Syntax error!' in str(context.exception))
    def test7(self):
        with self.assertRaises(Exception) as context:
            RegExp.RegExp('(u|k)){8}')
        self.assertTrue('Syntax error!' in str(context.exception))
    def test8(self):
        with self.assertRaises(Exception) as context:
            RegExp.RegExp('(u|k)oi]')
        self.assertTrue('Syntax error!' in str(context.exception))

class test_OR(unittest.TestCase):
    def _compile_(self):
        self.reg = None
    def test1(self):
        self.reg = RegExp.RegExp('u|k')
        self.assertEqual(self.reg.findall('uk'), ['u', 'k'])
    def test2(self):
        self.reg = RegExp.RegExp('ulj|koo|m')
        self.assertEqual(self.reg.findall('pkoo'), ['koo'])
    def test3(self):
        self.reg = RegExp.RegExp('ulj|m|(y|t)')
        self.assertEqual(self.reg.findall('tulj'), ['t', 'ulj'])
    def test4(self):
        self.reg = RegExp.RegExp('ulj|m|(y|t)')
        self.assertEqual(self.reg.findall('my'), ['m', 'y'])

class test_Cat(unittest.TestCase):
    def _compile_(self):
        self.reg = None
    def test1(self):
        self.reg = RegExp.RegExp('(uk|PP)hjk')
        self.assertEqual(self.reg.findall('PPhjk'), ['PPhjk'])
    def test2(self):
        self.reg = RegExp.RegExp('(uk|PP)hjk')
        self.assertEqual(self.reg.findall('PPhj'), [])
    def test3(self):
        self.reg = RegExp.RegExp('pptyr(idf)')
        self.assertEqual(self.reg.findall('pptyridf'), ['pptyridf'])

class test_Clini(unittest.TestCase):
    def _compile_(self):
        self.reg = None
    def test1(self):
        self.reg = RegExp.RegExp('(uk|P...)hjk...')
        self.assertEqual(self.reg.findall('PPhj'), ['PPhj'])
    def test2(self):
        self.reg = RegExp.RegExp('(P...)hjk')
        self.assertEqual(self.reg.findall('hjk'), ['hjk'])
    def test3(self):
        self.reg = RegExp.RegExp('(idf)...pptyr')
        self.assertEqual(self.reg.findall('idfidfpptyr'), ['idfidfpptyr'])
    def test4(self):
        self.reg = RegExp.RegExp('(i|d|f)...pptyr')
        self.assertEqual(self.reg.findall('idfidfpptyr'), ['idfidfpptyr'])
    def test5(self):
        self.reg = RegExp.RegExp('i...k...')
        self.assertEqual(self.reg.findall('iiiik'), ['i', 'i', 'i', 'i', 'k'])
class test_Repeat(unittest.TestCase):
    def _compile_(self):
        self.reg = None
    def test1(self):
        self.reg = RegExp.RegExp('(uk|P{1})hjk...')
        self.assertEqual(self.reg.findall('Phj'), ['Phj'])
    def test2(self):
        self.reg = RegExp.RegExp('(P...)hjk{3}')
        self.assertEqual(self.reg.findall('hjkkk'), ['hjkkk'])
    def test3(self):
        self.reg = RegExp.RegExp('((id)f{2})...pptyr')
        self.assertEqual(self.reg.findall('idffidffpptyr'), ['idffidffpptyr'])
    def test4(self):
        self.reg = RegExp.RegExp('(i|d|f{8})pptyr')
        self.assertEqual(self.reg.findall('ffffffffpptyr'), ['ffffffffpptyr'])
    def test5(self):
        self.reg = RegExp.RegExp('i{4}k...')
        self.assertEqual(self.reg.findall('iiiik'), ['iiii'])

class test_SqBrackets(unittest.TestCase):
    def _compile_(self):
        self.reg = None

    def test1(self):
        self.reg = RegExp.RegExp('(\\]|[um])jk')
        self.assertEqual(self.reg.findall(']jk'), [']jk'])

    def test2(self):
        self.reg = RegExp.RegExp('(P...)[hjk]...')
        self.assertEqual(self.reg.findall('hjk'), ['h','j','k'])

    def test3(self):
        self.reg = RegExp.RegExp('((id)ff)...([pty]|[r])h')
        self.assertEqual(self.reg.findall('idffphidffrh'), ['idffph', 'idffrh'])

    def test4(self):
        self.reg = RegExp.RegExp('[yo]|u')
        self.assertEqual(self.reg.findall('y'), ['y'])

    def test5(self):
        self.reg = RegExp.RegExp('i{5}[smt]')
        self.assertEqual(self.reg.findall('iiiiim'), ['iiiiim'])

class test_Comp(unittest.TestCase):
    def _compile_(self):
        self.reg = None

    def test1(self):
        self.reg = RegExp.RegExp('(h|[um])jk')
        tmp = self.reg.comlement()
        self.reg.automata = tmp
        self.assertEqual(self.reg.findall('mmhhk'), ['m','m','h','h','k'])

    def test2(self):
        self.reg = RegExp.RegExp('(hjk)...')
        tmp = self.reg.comlement()
        self.reg.automata = tmp
        self.assertEqual(self.reg.findall('hkj'), ['h','k','j'])

    def test3(self):
        self.reg = RegExp.RegExp('((id)ff)...([pty]|[r])h')
        tmp = self.reg.comlement()
        self.reg.automata = tmp
        self.assertEqual(self.reg.findall('ptg'), ['p', 't'])

class test_Diff(unittest.TestCase):
    def _compile_(self):
        self.reg = None

    def test1(self):
        self.reg = RegExp.RegExp('(h|u)hu')
        tmp = RegExp.RegExp('h|u')
        cur = self.reg.difference(tmp.automata, tmp.alphabet)
        self.reg.automata = cur
        self.assertEqual(self.reg.findall('huhhu'), ['hhu'])

    def test2(self):
        self.reg = RegExp.RegExp('(hjk)...')
        tmp = RegExp.RegExp('h|j|k')
        cur = self.reg.difference(tmp.automata, tmp.alphabet)
        self.reg.automata = cur
        self.assertEqual(self.reg.findall('hjk'), ['hjk'])

    def test3(self):
        self.reg = RegExp.RegExp('hjk')
        tmp = RegExp.RegExp('hjk')
        cur = self.reg.difference(tmp.automata, tmp.alphabet)
        self.reg.automata = cur
        self.assertEqual(self.reg.findall('hjk'), [])

    def test4(self):
        self.reg = RegExp.RegExp('[hj]u')
        tmp = RegExp.RegExp('h|u')
        cur = self.reg.difference(tmp.automata, tmp.alphabet)
        self.reg.automata = cur
        self.assertEqual(self.reg.findall('hu'), ['hu'])

class test_Rec(unittest.TestCase):
    def _compile_(self):
        self.reg = None

    def test1(self):
        self.reg = RegExp.RegExp('(a|bd...c)...bd...|(a|bd...c)...')
        tmp = self.reg.recovery()
        cur = RegExp.RegExp(tmp)
        self.assertEqual(self.reg.findall('abd'), cur.findall('abd'))

    def test2(self):
        self.reg = RegExp.RegExp('((kl|m)...)|[oi]')
        tmp = self.reg.recovery()
        cur = RegExp.RegExp(tmp)
        self.assertEqual(self.reg.findall('i'), cur.findall('i'))

    def test3(self):
        self.reg = RegExp.RegExp('kl...cd...')
        tmp = self.reg.recovery()
        cur = RegExp.RegExp(tmp)
        self.assertEqual(self.reg.findall('kcd'), cur.findall('kcd'))

    def test4(self):
        self.reg = RegExp.RegExp('h|ju...')
        tmp = self.reg.recovery()
        cur = RegExp.RegExp(tmp)
        self.assertEqual(self.reg.findall('juuuuu'), cur.findall('juuuuu'))

if __name__ == '__main__':
    unittest.main()