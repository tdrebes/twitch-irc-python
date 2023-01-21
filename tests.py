import unittest
import irc_bot

class TestReceiveData(unittest.TestCase):
    def test_read_messages(self):
        input = ':user1!user1@user1.tmi.twitch.tv PRIVMSG #channel :FeelsBadMan just throw it already..\r\n:user2!user2@user2.tmi.twitch.tv PRIVMSG #channel :forsenJAM \U000e0000\r\n:user3!user3@user3.tmi.twitch.tv PRIVMSG #channel :Clueless  TeaTime hmm...\r\n:user4!user4@user4.tmi.twitch.tv PRIVMSG #channel :forsenLaughingAtYou THROW forsenLaughingAtYou THROW forsenLaughingAtYou THROW\r\n'
        expectedParts = [
            ':user1!user1@user1.tmi.twitch.tv PRIVMSG #channel :FeelsBadMan just throw it already..', 
            ':user2!user2@user2.tmi.twitch.tv PRIVMSG #channel :forsenJAM \U000e0000', 
            ':user3!user3@user3.tmi.twitch.tv PRIVMSG #channel :Clueless  TeaTime hmm...', 
            ':user4!user4@user4.tmi.twitch.tv PRIVMSG #channel :forsenLaughingAtYou THROW forsenLaughingAtYou THROW forsenLaughingAtYou THROW',
        ]

        r1, r2 = irc_bot.read_messages(input, '')
        self.assertEqual(r1, expectedParts)
        self.assertEqual(r2, '')

    def test_read_messages_results_in_overflow(self):
        input = ':user1!user1@user1.tmi.twitch.tv PRIVMSG #channel :FeelsBadMan just throw it already..\r\n:user2!user2@user2.tmi.twitch.tv PRIVMSG #channel :forsenJAM \U000e0000\r\n:user3!user3@user3.tmi.twitch.tv PRIVMSG #channel :Clueless  TeaTime hmm...\r\n:user4!user4@user4.tmi.twitch.tv PRIVMSG #channel :forsenLaughingAtYou THROW forsenLaughingAtYou THROW fors'
        expectedParts = [
            ':user1!user1@user1.tmi.twitch.tv PRIVMSG #channel :FeelsBadMan just throw it already..', 
            ':user2!user2@user2.tmi.twitch.tv PRIVMSG #channel :forsenJAM \U000e0000', 
            ':user3!user3@user3.tmi.twitch.tv PRIVMSG #channel :Clueless  TeaTime hmm...', 
        ]
        
        r1, r2 = irc_bot.read_messages(input, '')
        self.assertEqual(r1, expectedParts)
        self.assertEqual(r2, ':user4!user4@user4.tmi.twitch.tv PRIVMSG #channel :forsenLaughingAtYou THROW forsenLaughingAtYou THROW fors')

    def test_read_messages_with_existing_overflow(self):
        input = 'BadMan just throw it already..\r\n:user2!user2@user2.tmi.twitch.tv PRIVMSG #channel :forsenJAM \U000e0000\r\n:user3!user3@user3.tmi.twitch.tv PRIVMSG #channel :Clueless  TeaTime hmm...\r\n:user4!user4@user4.tmi.twitch.tv PRIVMSG #channel :forsenLaughingAtYou THROW forsenLaughingAtYou THROW forsenLaughingAtYou THROW\r\n'
        expectedParts = [
            ':user1!user1@user1.tmi.twitch.tv PRIVMSG #channel :FeelsBadMan just throw it already..', 
            ':user2!user2@user2.tmi.twitch.tv PRIVMSG #channel :forsenJAM \U000e0000', 
            ':user3!user3@user3.tmi.twitch.tv PRIVMSG #channel :Clueless  TeaTime hmm...', 
            ':user4!user4@user4.tmi.twitch.tv PRIVMSG #channel :forsenLaughingAtYou THROW forsenLaughingAtYou THROW forsenLaughingAtYou THROW',
        ]

        r1, r2 = irc_bot.read_messages(input, ':user1!user1@user1.tmi.twitch.tv PRIVMSG #channel :Feels')
        self.assertEqual(r1, expectedParts)
        self.assertEqual(r2, '')

if __name__ == '__main__':
    unittest.main()
