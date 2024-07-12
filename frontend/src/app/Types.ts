export enum PieceType {
    PAWN = 'pawn',
    BISHOP = 'bishop',
    KNIGHT = 'knight',
    ROOK = 'rook',
    QUEEN = 'queen',
    KING = 'king',
}

// Define a class with a getter and setter for 'our'
export class TeamTypeManager {

    _our: number; // Default value for 'our'
    _opponent: number; // Default value for 'opponent'
    
    constructor(our: string) {
      this._our = our === 'w' ? 1 : 2;
      this._opponent = our === 'w' ? 2 : 1;
    }
    // Getter for 'our'
    get our(): number {
      return this._our;
    }
  
    // Setter for 'our'
    set our(value: string) {
      this._our = value === 'w' ? 1 : 2;
    }
    set opponent(value: string) {
      this._opponent = value === 'w' ? 2 : 1;
    }
    // Function to determine the value of 'OPPONENT' based on 'our'
    get opponent(): number {
      return this._opponent;
    }
  }

export const TeamTypeManager_ = new TeamTypeManager('w');

export enum TeamType {
    OPPONENT = TeamTypeManager_.opponent,
    OUR = TeamTypeManager_.our,
    DRAW = 3,
}
