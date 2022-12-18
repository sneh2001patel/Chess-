# Chess
<hr/>

__TODO:__

- [X] Other pieces cannot move if the king is checked
- [X] Check where the check is coming from and check if any pieces can block it, if it can block show it has a valid move it can take
- [X] A king cannot kill a piece if the next move will result in a check (Only need to worry about this case with the king's kills)
- [X] It is a checkmate if the king is in check and has no valid moves
- [ ] Add Castlo (additional feat)
- [X] Make it so that when pawn reaches end of the board pawn can change into any other piece (Rook, Queen, Bishop, Knight)
- [X] Make it so that pieces wont move from there spot if the destation position leads to thier king getting checked
- Problem might be that other times when `direction()` is called board is defined check it out
- [ ] Fix this error `AttributeError: 'NoneType' object has no attribute 'all_position'`