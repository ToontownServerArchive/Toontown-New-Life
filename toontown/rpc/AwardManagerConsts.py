#Embedded file name: toontown.rpc.AwardManagerConsts
GiveAwardErrors = Enum('Success, WrongGender, NotGiftable, FullMailbox, FullAwardMailbox, AlreadyInMailbox, AlreadyInGiftQueue, AlreadyInOrderedQueue, AlreadyInCloset, AlreadyBeingWorn, AlreadyInAwardMailbox, AlreadyInThirtyMinuteQueue, AlreadyInMyPhrases, AlreadyKnowDoodleTraining, AlreadyRented, GenericAlreadyHaveError, UnknownError, UnknownToon, NonToon,')
GiveAwardErrorStrings = {GiveAwardErrors.Success: 'Success',
 GiveAwardErrors.WrongGender: 'Wrong gender',
 GiveAwardErrors.NotGiftable: 'Item is not giftable',
 GiveAwardErrors.FullMailbox: 'Mailbox is full',
 GiveAwardErrors.FullAwardMailbox: 'Award mailbox is full',
 GiveAwardErrors.AlreadyInMailbox: 'Award already in mailbox.',
 GiveAwardErrors.AlreadyInGiftQueue: 'Award already in gift queue.',
 GiveAwardErrors.AlreadyInOrderedQueue: 'Award already in ordered queue.',
 GiveAwardErrors.AlreadyInCloset: 'Award already in closet.',
 GiveAwardErrors.AlreadyBeingWorn: 'Award already being worn.',
 GiveAwardErrors.AlreadyInAwardMailbox: 'Award already in award mailbox',
 GiveAwardErrors.AlreadyInThirtyMinuteQueue: 'Award already in 30 minute queue',
 GiveAwardErrors.AlreadyInMyPhrases: 'Speec Chat Award already in my phrases',
 GiveAwardErrors.AlreadyKnowDoodleTraining: 'Doodle Training Award already known',
 GiveAwardErrors.AlreadyRented: 'Award is already rented',
 GiveAwardErrors.GenericAlreadyHaveError: 'Generic-Already-Have error',
 GiveAwardErrors.UnknownError: 'Unknown error',
 GiveAwardErrors.UnknownToon: 'Toon not in database',
 GiveAwardErrors.NonToon: 'This is not a toon'}
