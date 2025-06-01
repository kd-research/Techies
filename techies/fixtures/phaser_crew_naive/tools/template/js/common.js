/**
 * Displays a labeled numeric value on screen, with methods to
 * increment and reset it.  Shows at most one digit after the
 * decimal if the value isn’t an integer.
 */
class MetricDisplay {
    /**
     * @param {Phaser.Scene} scene
     * @param {number} x
     * @param {number} y
     * @param {string} label
     * @param {number} initial   Starting value (default 0)
     * @param {object} style
     */
    constructor(scene, x, y, label, initial = 0, style = { fontSize: '24px', fill: '#000', fontStyle: 'bold' }) {
        this.scene = scene;
        this.value = initial;
        this.label = label;
        this.text = scene.add.text(x, y, `${label}: ${this._fmt(initial)}`, style);
        this.text.setScrollFactor(0);
    }

    /**
     * Add to the current value and update the display.
     * @param {number} delta
     */
    add(delta) {
        this.value += delta;
        this.text.setText(`${this.label}: ${this._fmt(this.value)}`);
    }

    /** Reset the value to zero and update the display. */
    reset() {
        this.value = 0;
        this.text.setText(`${this.label}: ${this._fmt(this.value)}`);
    }

    /**
     * Format a number: if it's an integer, no decimals;
     * otherwise one digit after decimal point.
     * @param {number} v
     * @returns {string}
     * @private
     */
    _fmt(v) {
        return Number.isInteger(v)
            ? v.toString()
            : v.toFixed(1);
    }
}

class TextDisplay {
    /**
     * @param {Phaser.Scene} scene
     * @param {number} x
     * @param {number} y
     * @param {string} text
     * @param {object} style
     */
    constructor(scene, x, y, text, style = { fontSize: '24px', fill: '#000', fontStyle: 'bold' }) {
        this.scene = scene;
        this.text = scene.add.text(x, y, text, style);
        this.text.setScrollFactor(0);
    }

    setText(text) {
        this.text.setText(text);
    }
}


/**
 * A single enemy sprite that automatically chases a target (the player).
 */
class ChasingEnemy extends Phaser.Physics.Arcade.Sprite {
    /**
     * @param {Phaser.Scene} scene
     * @param {number} x
     * @param {number} y
     * @param {string} idleTexture    Key of the loaded image/spritesheet.
     * @param {string} runTexture     Key of the loaded image/spritesheet.
     * @param {Phaser.Physics.Arcade.Sprite} target
     * @param {number} speed      Horizontal chase speed.
     */
    constructor(scene, x, y, idleTexture, runTexture, target, speed = 100) {
        super(scene, x, y, idleTexture);
        this.scene = scene;
        this.target = target;
        this.speed = speed;

        scene.add.existing(this);
        scene.physics.add.existing(this);

        // gravity so it lands on platforms
        this.setBounce(0.2);

        // create idle animation
        this.anims.create({
            key: 'enemy_idle',
            frames: scene.anims.generateFrameNumbers(idleTexture),
            frameRate: 20,
            repeat: -1
        });
        this.anims.create({
            key: 'enemy_run',
            frames: scene.anims.generateFrameNumbers(runTexture),
            frameRate: 20,
            repeat: -1
        });
    }

    /** Call this each frame in your scene.update() */
    update() {
        let diff_x = this.target.x - this.x;

        // disable if the target is too far away
        if (Math.abs(diff_x) > 300) {
            this.setVelocityX(0);
            this.anims.play('enemy_idle', true);
            return;
        } 

        // simple horizontal chase
        if (Math.abs(diff_x) < 10) {
            this.setVelocityX(0);
            this.anims.play('enemy_idle', true);
        } else {
            this.setVelocityX(diff_x < 0 ? -this.speed : this.speed);
            this.anims.play('enemy_run', true);
        }
        // flip the sprite to face the target
        // (this assumes the sprite faces right by default)
        this.setFlipX(diff_x < 0);

        // flip Y based on world gravity
        this.setFlipY(this.scene.physics.world.gravity.y < 0);
        

        // if the enemy is blocked by a tile, try jumping
        if (this.body.blocked.left || this.body.blocked.right) {
            // jump based on gravity direction
            if (this.scene.physics.world.gravity.y > 0) {
                this.setVelocityY(-300);
            } else {
                this.setVelocityY(300);
            }
        }
    }
}


/**
 * Represents a gamepad button in a Phaser scene.
 * 
 * @class
 * @param {Phaser.Scene} scene - The Phaser scene where the button will be added.
 * @param {number} x - The x-coordinate of the button.
 * @param {number} y - The y-coordinate of the button.
 * @param {string} text - The text to display on the button.
 * @param {Function} callback - The function to call when the button is clicked.
 */
class GamepadButton {
    constructor(scene, x, y, text, callback) {
        this.scene = scene;
        this.x = x;
        this.y = y;
        this.text = text;
        this.callback = callback;
        this.button = scene.add.text(x, y, text, { fontSize: '32px', fill: '#fff' })
            .setOrigin(0.5)
            .setInteractive()
            .setScrollFactor(0)
            .on('pointerdown', () => {
                this.callback();
            })
    }
}

/**
 * A control panel overlay for a game, containing a background panel, a virtual joystick,
 * and configurable gamepad buttons.
 *
 * Functions:
 * - constructor(scene, mapHeight, gameHeight, gameWidth): Initializes the control panel with a background and joystick.
 * - setButtons(texts, callbacks): Creates and places on-screen gamepad buttons.
 */
class GameControlPanel {
    /**
     * Creates an instance of GameControlPanel.
     *
     * @param {Phaser.Scene} scene - The Phaser scene to which the control panel belongs.
     * @param {number} mapHeight - The height in pixels of the game map (top portion of the game).
     * @param {number} gameHeight - The total height in pixels of the game canvas.
     * @param {number} gameWidth - The total width in pixels of the game canvas.
    */
    constructor(scene, mapHeight, gameHeight, gameWidth) {
        this.scene = scene;
        this.mapHeight = mapHeight;
        this.gameHeight = gameHeight;
        this.gameWidth = gameWidth;

        // add black background
        this.background = scene.add.rectangle(0, mapHeight, gameWidth, gameHeight - mapHeight, 0x000000)
            .setOrigin(0)
            .setScrollFactor(0);
        
        // add a virtual joystick
        var joystickPlugin = this.scene.plugins.get('rexvirtualjoystickplugin');
        var joystick = joystickPlugin.add(this.scene, {
            x: 120,
            y: mapHeight + (gameHeight - mapHeight) * 0.5,
            radius: 70,
            dir: 'left&right',
        }); 
        this.joystick = joystick;
        
    }

    /**
     * Creates and places on-screen gamepad buttons.
     *
     * @param {string[]} texts - An array of labels for each button.
     * @param {Function[]} callbacks - An array of callback functions invoked when each button is pressed.
     * @returns {GamepadButton[]} An array of the created GamepadButton instances.
     */
    setButtons(texts, callbacks) {
        const buttonNumber = texts.length;
        const panelHeight = this.gameHeight - this.mapHeight;

        // calculate button x and y positions
        const x_pos = this.gameWidth - 100;
        var y_pos = [];
        for (let i = 0; i < buttonNumber; i++) {
            y_pos.push(this.mapHeight + (panelHeight / (buttonNumber + 1)) * (i + 1));
        }
        // create buttons
        var buttons = [];
        for (let i = 0; i < buttonNumber; i++) {
            const button = new GamepadButton(this.scene, x_pos, y_pos[i], texts[i], callbacks[i]);
            buttons.push(button);
        }
        return buttons;
    }
}


/**
 * The GameOver class handles the logic for ending the game, including pausing physics,
 * displaying a "Game Over" message, and applying visual effects to the player.
 * 
 * Functions:
 * - constructor(scene): Initializes the GameOver instance with a Phaser scene.
 * - run(message): Ends the game and displays a message.
 */
class GameOver {
    /**
     * @param {Phaser.Scene} scene
     */
    constructor(scene) {
        this.scene = scene;
        this.ended = false;
    }

    run(message = 'GAME OVER') {
        this.ended = true;

        // pause all physics
        this.scene.physics.pause();

        // tint the player red
        this.scene.player.setTint(0xff0000);

        // show a centered Game Over message
        const w = this.scene.scale.width;
        const h = this.scene.scale.height;
        this.scene.add
            .text(w/2, h/2, message, {
                fontSize: '64px',
                fill: '#f00',
                fontStyle: 'bold'
            })
            .setOrigin(0.5)
            .setScrollFactor(0);
    }
}