import unittest
from grouping import assign_balanced_groups

class TestAssignBalancedGroups(unittest.TestCase):
    def test_even_distribution(self):
        singles = ["A", "B", "C", "D"]
        doubles = ["X", "Y"]
        n_groups = 3
        # Total weight = 4 + 4 = 8, should be distributed as evenly as possible
        groups = assign_balanced_groups(singles, doubles, n_groups)
        weights = sorted(group['weight'] for group in groups)
        self.assertTrue(max(weights) - min(weights) <= 1)

    def test_overlapping_names(self):
        singles = ["A", "B", "X"]
        doubles = ["X", "Y"]
        n_groups = 2
        # X should only be counted as double
        groups = assign_balanced_groups([s for s in singles if s != "X"], doubles, n_groups)
        total_names = [name for group in groups for name, _ in group['members']]
        self.assertNotIn("X", [name for name in singles if name not in doubles])
        self.assertIn("X", total_names)
        # Total weight should be 1 (A) + 1 (B) + 2 (X) + 2 (Y) = 6
        self.assertEqual(sum(group['weight'] for group in groups), 6)

    def test_all_doubles(self):
        singles = []
        doubles = ["A", "B", "C", "D"]
        n_groups = 2
        groups = assign_balanced_groups(singles, doubles, n_groups)
        weights = [group['weight'] for group in groups]
        # 4 doubles = total weight 8, should be 4+4
        self.assertEqual(sorted(weights), [4, 4])

    def test_all_singles(self):
        singles = ["A", "B", "C", "D"]
        doubles = []
        n_groups = 2
        groups = assign_balanced_groups(singles, doubles, n_groups)
        weights = [group['weight'] for group in groups]
        self.assertEqual(sorted(weights), [2, 2])

    def test_randomness(self):
        # With randomness, test runs shouldn't always return the same assignments
        singles = [f"Single{i}" for i in range(6)]
        doubles = [f"Double{i}" for i in range(3)]
        n_groups = 3
        results = []
        for _ in range(10):
            groups = assign_balanced_groups(singles, doubles, n_groups)
            names_per_group = [tuple(sorted(name for name, _ in group['members'])) for group in groups]
            results.append(tuple(sorted(names_per_group)))
        self.assertGreater(len(set(results)), 1)  # At least 2 different groupings in 10 tries

if __name__ == "__main__":
    unittest.main()