# -*- coding: utf-8; -*-

# Copyright (C) 2015 - 2020 Lionel Ott
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>


import sys
sys.path.append("..")

import pytest

import gremlin.error
from gremlin.tree import TreeNode


def test_constructor():
    n1 = TreeNode(1)
    assert n1.value == 1
    assert n1.children == []
    assert n1.parent == None

    n2 = TreeNode(2, None)
    assert n2.value == 2
    assert n2.children == []
    assert n2.parent == None

    n3 = TreeNode(3, n1)
    assert n3.value == 3
    assert n3.children == []
    assert n3.parent == n1
    assert n1.children == [n3]


def test_add_child():
    n1 = TreeNode(1)
    n2 = TreeNode(2)
    n3 = TreeNode(3)
    n4 = TreeNode(4)

    n1.add_child(n2)
    assert n1.children == [n2]
    assert n2.parent == n1

    n1.add_child(n3)
    assert n1.children == [n2, n3]
    assert n3.parent == n1

    n1.add_child(n4)
    assert n1.children == [n2, n3, n4]
    assert n4.parent == n1

def test_add_sibling():
    n1 = TreeNode(1)
    n2 = TreeNode(2)
    n3 = TreeNode(3)
    n4 = TreeNode(4)

    with pytest.raises(gremlin.error.GremlinError):
        n1.add_sibling(n2)
        assert n1.children == []

    n1.add_child(n2)
    assert n1.children == [n2]
    assert n2.parent == n1

    n2.add_sibling(n3)
    assert n1.children == [n2, n3]
    assert n2.children == []
    assert n3.parent == n1

    n2.add_sibling(n4)
    assert n1.children == [n2, n3, n4]
    assert n2.children == []
    assert n4.parent == n1


def test_set_parent():
    n1 = TreeNode(1)
    n2 = TreeNode(2)
    assert n1.parent == None
    assert n2.parent == None

    n2.set_parent(n1)
    assert n1.parent == None
    assert n2.parent == n1
    assert n1.children == [n2]
    assert n2.children == []

    with pytest.raises(gremlin.error.GremlinError):
        n1.set_parent(n2)
        assert n1.parent == None
        assert n2.parent == n1
        assert n1.children == [n2]
        assert n2.children == []

    n2.detach()
    assert n1.parent == None
    assert n2.parent == None
    assert n1.children == []
    assert n2.children == []

    n1.set_parent(n2)
    assert n1.parent == n2
    assert n2.parent == None
    assert n1.children == []
    assert n2.children == [n1]


def test_remove_child():
    n1 = TreeNode(1)
    n2 = TreeNode(2, n1)
    n3 = TreeNode(3, n1)
    n4 = TreeNode(4, n2)
    n5 = TreeNode(5, n2)

    assert n1.parent == None
    assert n1.children == [n2, n3]
    assert n2.parent == n1
    assert n2.children == [n4, n5]
    assert n3.parent == n1
    assert n3.children == []
    assert n4.parent == n2
    assert n4.children == []
    assert n5.parent == n2
    assert n5.children == []

    n2.remove_child(n5)
    assert n2.parent == n1
    assert n2.children == [n4]
    assert n5.parent == None
    assert n5.children == []

    n1.remove_child(n2)
    assert n1.parent == None
    assert n1.children == [n3]
    assert n2.parent == None
    assert n2.children == [n4]
    assert n5.parent == None
    assert n5.children == []


def test_detach():
    n1 = TreeNode(1)
    n2 = TreeNode(2, n1)
    n3 = TreeNode(3, n1)
    n4 = TreeNode(4, n2)
    n5 = TreeNode(5, n2)

    assert n1.parent == None
    assert n1.children == [n2, n3]
    assert n2.parent == n1
    assert n2.children == [n4, n5]
    assert n3.parent == n1
    assert n3.children == []
    assert n4.parent == n2
    assert n4.children == []
    assert n5.parent == n2
    assert n5.children == []

    n2.detach()
    assert n1.parent == None
    assert n1.children == [n3]
    assert n2.parent == None
    assert n2.children == [n4, n5]

    n1.detach()
    assert n1.parent == None
    assert n1.children == [n3]

    n5.detach()
    assert n2.parent == None
    assert n2.children == [n4]
    assert n5.parent == None
    assert n5.children == []


def test_is_descendant():
    n1 = TreeNode(1)
    n2 = TreeNode(2, n1)
    n3 = TreeNode(3, n1)
    n4 = TreeNode(4, n2)
    n5 = TreeNode(5, n2)
    n6 = TreeNode(6)

    assert n1.parent == None
    assert n1.children == [n2, n3]
    assert n2.parent == n1
    assert n2.children == [n4, n5]
    assert n3.parent == n1
    assert n3.children == []
    assert n4.parent == n2
    assert n4.children == []
    assert n5.parent == n2
    assert n5.children == []

    assert n1.is_descendant(n5) == True
    assert n5.is_descendant(n1) == False
    assert n1.is_descendant(n6) == False
    assert n6.is_descendant(n1) == False
    assert n2.is_descendant(n3) == False
    assert n3.is_descendant(n3) == False
    assert n2.is_descendant(n4) == True
    assert n4.is_descendant(n2) == False