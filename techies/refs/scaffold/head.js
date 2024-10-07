if Platform.majorVersion() != 1 
{
    throw "This script requires Platform version 1.x";
}

// Platform version 1.x provides the following functions:
// All numbers are integer numbers
// Platform.majorVersion() => number
// Platform.minorVersion() => number
// Platform.setHighestScore(score: number) => void
// Platform.getHighestScore() => number
// Platform.getSoundVolume() => number // in range [0-100]
// Platform.getPreferredDifficulty() => number  // 0 = easy, 1 = medium, 2 = hard, 3 = default
