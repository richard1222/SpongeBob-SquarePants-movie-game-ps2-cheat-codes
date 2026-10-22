"""Regression for wrapped PowerShell errors; no game files or PowerShell needed."""
import unittest
from test_patchers import message_matches

class ErrorMessageTests(unittest.TestCase):
    def test_reported_existing_output_failure(self):
        output='Apply.ps1 : Output already\nexists. It was not overwritten.\r\n'
        self.assertNotIn('already exists',output.lower())
        self.assertTrue(message_matches('already exists',output))

    def test_crlf_and_indentation(self):
        self.assertTrue(message_matches('Source code guard','Source\r\n    code\tguard failed.'))

    def test_case_insensitive(self):
        self.assertTrue(message_matches('wrong source','WRONG SOURCE.'))

    def test_normalize_expected_too(self):
        self.assertTrue(message_matches('hash\t mismatch','Output hash mismatch.'))

    def test_wrong_error_is_still_wrong(self):
        self.assertFalse(message_matches('already exists','Wrong source.'))

    def test_does_not_join_broken_words(self):
        self.assertFalse(message_matches('already exists','alrea\ndy exists'))

    def test_does_not_drop_intervening_words(self):
        self.assertFalse(message_matches('output hash mismatch','output has no hash mismatch'))

    def test_missing_message_fails(self):
        self.assertFalse(message_matches('already exists',''))

if __name__=='__main__':unittest.main()
