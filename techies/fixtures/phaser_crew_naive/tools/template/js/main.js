/**
 * A simple bullet sprite that can be shot left or right.
 */
class Bullet extends Phaser.Physics.Arcade.Image {
    /**
     * @param {Phaser.Scene} scene
     */
    constructor(scene) {
        super(scene, 0, 0, 'bullet');
        scene.add.existing(this);
        scene.physics.add.existing(this);
        this.setCollideWorldBounds(true);
        this.body.onWorldBounds = true; // auto-disable when off‐screen
        this.setGravityY(0);
    }

    /**
     * Activate and send the bullet.
     * @param {number} x
     * @param {number} y
     * @param {'left'|'right'} direction
     */
    shoot(x, y, direction) {
        this.enableBody(true, x, y, true, true);
        const speed = 400;
        this.setVelocityX(direction === 'left' ? -speed : speed);
    }
}

/**
 * A pool of Bullet instances.
 */
class BulletGroup extends Phaser.Physics.Arcade.Group {
    /**
     * @param {Phaser.Scene} scene
     */
    constructor(scene) {
        super(scene.physics.world, scene);

        this.createMultiple({
            classType: Bullet,
            frameQuantity: 20,
            active: false,
            visible: false,
            key: 'bullet'
        });
    }

    /**
     * Fire one bullet from the pool.
     * @param {number} x
     * @param {number} y
     * @param {'left'|'right'} direction
     */
    fire(x, y, direction) {
        const b = this.getFirstDead(false);
        if (b) {
            b.shoot(x, y, direction);
        }
    }
}

/**
 * Listens for a key (default 'F') and tells a BulletGroup to fire
 * based on the player's facing direction.
 */
class Shooter {
    /**
     * @param {Phaser.Scene} scene
     * @param {BasePlayer} player
     * @param {BulletGroup} bullets
     * @param {string} key        Phaser key name, e.g. 'F'
     */
    constructor(scene, player, bullets, key = 'F') {
        this.scene = scene;
        this.player = player;
        this.bullets = bullets;
        this.fireKey = scene.input.keyboard.addKey(Phaser.Input.Keyboard.KeyCodes[key]);
    }

    /** Call every frame in your scene.update() */
    update() {
        if (Phaser.Input.Keyboard.JustDown(this.fireKey)) {
            this.fire();  // fire a bullet
        }
    }

    fire() {
        const { x, y, displayWidth, displayHeight, facing } = this.player;
        const offsetX = facing === 'left' ? -10 : displayWidth + 10;
        this.bullets.fire(x + offsetX, y, facing);
    }
}

/**
 * A player sprite that can move left/right and jump.
 * Automatically sets up animations for a given texture key.
 */
class BasePlayer extends Phaser.Physics.Arcade.Sprite {
    /**
     * @param {Phaser.Scene} scene
     * @param {object} joystick
     * @param {number} x
     * @param {number} y
     * @param {string} texture   Key of the loaded sprite sheet.
     * @param {string} idleTexture   Key of the loaded sprite sheet.
     */
    constructor(scene, joystick, x, y, texture, idleTexture=null) {
        if (idleTexture === null) {
            idleTexture = texture;
        }
        super(scene, x, y, texture);
        scene.add.existing(this);
        scene.physics.add.existing(this);

        // cursors for left/right, plus a separate key for jump
        this.cursors = scene.input.keyboard.createCursorKeys();
        this.gamepadKeys = joystick.createCursorKeys();
        this.jumpKey = scene.input.keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.SPACE);

        this.facing = 'right';

        // run animation
        scene.anims.create({
            key: 'run',
            frames: scene.anims.generateFrameNumbers(texture),
            frameRate: 20,
            repeat:    -1
        });
        // idle animation
        scene.anims.create({
            key: 'idle',
            frames: scene.anims.generateFrameNumbers(idleTexture),
            frameRate: 20,
            repeat:    -1
        });

    }

    /** Call this each frame in Scene.update() */
    update() {
        const { left, right } = this.cursors;
        var leftKeyDown = this.gamepadKeys.left.isDown;
        var rightKeyDown = this.gamepadKeys.right.isDown;

        // Horizontal movement
        if (left.isDown || leftKeyDown) {
            this.setVelocityX(-160);
            this.anims.play('run', true);
            this.flipX = true;  // flip the sprite to face left
            this.facing = 'left';
        } else if (right.isDown || rightKeyDown) {
            this.setVelocityX(160);
            this.anims.play('run', true);
            this.flipX = false; // face right
            this.facing = 'right';
        } else {
            this.setVelocityX(0);
            this.anims.play('idle', true);
        }

        // Jump on SPACE
        if (this.jumpKey.isDown) {
            this.jump();
        }
    }

    jump() {    
        if (this.body.blocked.down) {
            this.setVelocityY(-330);
        }
    }
}


/**
 * A physics group of collectible stars (or other sprites) that bounce.
 */
class CollectibleGroup {
    /**
     * @param {Phaser.Scene} scene
     * @param {string} key           Texture key for the sprite.
     * @param {number} repeat        How many extras to spawn (repeat+1 total).
     * @param {{ x: number, y: number, stepX: number }} setXY
     */
    constructor(scene, key, repeat, setXY) {
        this.group = scene.physics.add.group({
            key,
            repeat,
            setXY
        });
        this.group.children.iterate(child => {
            child.setBounceY(Phaser.Math.FloatBetween(0.1, 0.3));
        });
    }
}

/**
 * Handles overlap between a player and a collectible group,
 * updating a MetricDisplay when items are collected.
 */
class Collector {
    /**
     * @param {Phaser.Scene} scene
     * @param {Phaser.GameObjects.Sprite} player
     * @param {Phaser.Physics.Arcade.Group} collectibles
     * @param {MetricDisplay} scoreDisplay
     * @param {number} pointsPerItem
     */
    constructor(scene, player, collectibles, scoreDisplay, pointsPerItem = 10) {
        this.scoreDisplay = scoreDisplay;
        this.points = pointsPerItem;
        scene.physics.add.overlap(player, collectibles, (p, item) => {
            item.disableBody(true, true);
            this.scoreDisplay.add(this.points);
        });
    }
}


/**
 * A pool of static, immovable enemies.
 */
class EnemyGroup {
    /**
     * @param {Phaser.Scene} scene
     * @param {Array<{ x: number, y: number, key: string, scale?: number }>} configs
     */
    constructor(scene, configs) {
        this.group = scene.physics.add.group({
            allowGravity: false,
            immovable: true
        });
        // add enemy idle animation
        scene.anims.create({
            key: 'enemy_idle',
            frames: scene.anims.generateFrameNumbers('enemy_idle'),
            frameRate: 10,
            repeat: -1
        });
        configs.forEach(cfg => {
            const e = this.group.create(cfg.x, cfg.y, cfg.key);
            e.play('enemy_idle');
            if (cfg.scale) e.setScale(cfg.scale).refreshBody();
        });
    }
}

/**
 * Static apples placed in the world that the player can collect.
 */
class AppleGroup {
    /**
     * @param {Phaser.Scene} scene
     * @param {Array<{ x: number, y: number, key: string, scale?: number }>} configs
     */

    constructor(scene, configs) {
        // apple idle animation
        scene.anims.create({
            key: 'apple',
            frames: scene.anims.generateFrameNumbers('apple'),
            frameRate: 20,
            repeat: -1
        });

        this.group = scene.physics.add.staticGroup();
        configs.forEach(cfg => {
            const apple = this.group.create(cfg.x, cfg.y, cfg.key);
            apple.play('apple');
            if (cfg.scale) {
                apple.setScale(cfg.scale).refreshBody();
            }
        });
    }
}

/**
 * When the player overlaps an apple, grant temporary immunity,
 * and drive a MetricDisplay countdown of the remaining seconds.
 */
class ImmunityPowerUp {
    /**
     * @param {Phaser.Scene} scene
     * @param {Phaser.Physics.Arcade.Sprite} player
     * @param {Phaser.Physics.Arcade.Group|Phaser.GameObjects.Group} apples
     * @param {MetricDisplay} immunityDisplay   Display to show remaining seconds
     * @param {number} duration              Milliseconds of immunity (default 15000)
     */
    constructor(scene, player, apples, immunityDisplay, duration = 15000) {
        this.scene = scene;
        this.player = player;
        this.apples = apples;
        this.display = immunityDisplay;
        this.duration = duration;
        this.player.immunity = false;

        scene.physics.add.overlap(player, apples, (pl, apple) => {
            apple.disableBody(true, true);
            this._activate();
        });
    }

    _activate() {
        if (this.player.immunity) return;
        this.player.immunity = true;
        this.player.setTint(0xFFD251);

        const totalSecs = Math.floor(this.duration / 1000);

        // reset & start the display at totalSecs
        this.display.reset();
        this.display.add(totalSecs);

        // every second subtract 1
        this.countdownEvent = this.scene.time.addEvent({
            delay: 1000,
            repeat: totalSecs - 1,
            callback: () => this.display.add(-1)
        });

        // when time's up, end immunity & clear display
        this.scene.time.delayedCall(this.duration, () => {
            this.player.immunity = false;
            this.player.clearTint();
            this.display.reset();
        });
    }
}


/**
 * When player touches any enemy, subtract health—
 * but skip if player is currently immune.
 */
class DamageOnTouch {
    /**
     * @param {Phaser.Scene} scene
     * @param {Phaser.Physics.Arcade.Sprite} player
     * @param {Phaser.Physics.Arcade.Group|Phaser.GameObjects.Group|Phaser.Physics.Arcade.Sprite} enemies
     * @param {MetricDisplay} healthDisplay
     * @param {number} damage   How much health to subtract
     */
    constructor(scene, player, enemies, healthDisplay, damage = 10) {
        this.healthDisplay = healthDisplay;
        scene.physics.add.overlap(player, enemies, () => {
            if (!player.immunity) {
                this.healthDisplay.add(-damage);
            }
        });
    }
}


/**
 * When a bullet hits an enemy, both are disabled and you get points.
 */
class BulletEnemyCollision {
    /**
     * @param {Phaser.Scene} scene
     * @param {BulletGroup} bullets
     * @param {Phaser.Physics.Arcade.Group} enemies
     * @param {MetricDisplay} scoreDisplay   Display to credit points to
     * @param {number} pointsPerKill       How many points per enemy (default 10)
     */
    constructor(scene, bullets, enemies, scoreDisplay, pointsPerKill = 10) {
        this.scoreDisplay = scoreDisplay;
        this.points       = pointsPerKill;

        scene.physics.add.overlap(bullets, enemies, (bullet, enemy) => {
            bullet.disableBody(true, true);
            enemy.disableBody(true, true);
            this.scoreDisplay.add(this.points);
        });
    }
}


/**
 * Ends the game when the linked health display goes below zero.
 */
class GameOverOnHealth {
    /**
     * @param {Phaser.Scene} scene
     * @param {MetricDisplay} healthDisplay
     */
    constructor(scene, healthDisplay) {
        this.scene = scene;
        this.healthDisplay = healthDisplay;
        this.ended = false;
    }

    /** Call every frame in your scene.update() */
    update() {
        if (!this.ended && this.healthDisplay.value <= 0) {
            this.ended = true;

            // pause all physics
            this.scene.physics.pause();

            // tint the player red
            this.scene.player.setTint(0xff0000);

            // show a centered Game Over message
            const w = this.scene.scale.width;
            const h = this.scene.scale.height;
            this.scene.add
                .text(w/2, h/2, 'GAME OVER', {
                    fontSize: '64px',
                    fill: '#f00',
                    fontStyle: 'bold'
                })
                .setOrigin(0.5)
                .setScrollFactor(0);
        }
    }
}

/**
 * A static goal object that the player can reach to win the game.
 */
class Destination {
    /**
     * @param {Phaser.Scene} scene
     * @param {Phaser.Physics.Arcade.Sprite} player
     * @param {number} x            X position of the goal
     * @param {number} y            Y position of the goal
     * @param {string} key          Texture key for the goal sprite
     */
    constructor(scene, player, x, y, key) {
        this.scene = scene;
        this.player = player;
        this.reached = false;
        this.sprite = scene.physics.add.staticImage(x, y, key);
    }

    onReach() {
        if (this.reached) return;
        this.reached = true;
        this.scene.gameOver.run("YOU WIN!");
    }
}


class MainScene extends Phaser.Scene {
    constructor() {
        super({ key: 'MainScene' });
    }

    preload() {
        window.defaultScene = this;  // for high-level access
        this.load.setBaseURL('assets/');
        this.load.image('star', 'star.png');
        this.load.image('bullet', 'bomb.png');
        this.load.image('flag', 'Pixel_Adventure/Items/Checkpoints/End/End (Idle).png');    // <-- load flag sprite
        this.load.image('ground_1x1', 'ground_1x1.png');
        this.load.tilemapTiledJSON('map', 'level1.json');
        this.load.spritesheet('player_run', 'Pixel_Adventure/Main Characters/Virtual Guy/Run (32x32).png', {
            frameWidth: 32,
            frameHeight: 32
        });
        this.load.spritesheet('player_idle', 'Pixel_Adventure/Main Characters/Virtual Guy/Idle (32x32).png', {
            frameWidth: 32,
            frameHeight: 32
        });
        this.load.spritesheet('apple', 'Pixel_Adventure/Items/Fruits/Apple.png', {
            frameWidth: 32,
            frameHeight: 32
        });
        this.load.spritesheet('enemy_idle', 'Pixel_Adventure/Main Characters/Ninja Frog/Idle (32x32).png', {
            frameWidth: 32,
            frameHeight: 32
        });
        this.load.spritesheet('enemy_run', 'Pixel_Adventure/Main Characters/Ninja Frog/Run (32x32).png', {
            frameWidth: 32,
            frameHeight: 32
        });
        this.load.plugin({
            key: 'rexvirtualjoystickplugin',
            url: 'https://raw.githubusercontent.com/rexrainbow/phaser3-rex-notes/master/dist/rexvirtualjoystickplugin.min.js',
            sceneKey: 'rexUI'
        });
    }

    create() {

        // load game tile map
        this.map = this.add.tilemap('map');
        const tiles = this.map.addTilesetImage('ground_1x1');
        const tileLayer = this.map.createLayer("Tile Layer", tiles, 0, 0);
        tileLayer.setCollisionByProperty({ type: [ 'ground' ] });

        const gameWidth = window.innerWidth - 0;
        const gameHeight = window.innerHeight - 65;
        const mapHeight = tileLayer.height;
        // add control panel
        const controlPanel = new GameControlPanel(this, mapHeight, gameHeight, gameWidth);

        // player
        this.player = new BasePlayer(this, controlPanel.joystick, 100, 450, 'player_run', 'player_idle');
        this.physics.add.collider(this.player, tileLayer);

        // set the camera to follow the player
        this.cameras.main.startFollow(this.player);
        this.cameras.main.setBounds(0, 0, tileLayer.x + tileLayer.width + 600, 0);

        // load game over
        this.gameOver = new GameOver(this);

        // --- From this line below is customizable ---

        // collect stars to increase score
        this.stars        = new CollectibleGroup(this, 'star', 14, { x: 250, y: 50, stepX: 90 });
        this.physics.add.collider(this.stars.group, tileLayer);
        this.scoreDisplay = new MetricDisplay(this, 16, 16,   'Score');
        this.collector    = new Collector(this, this.player, this.stars.group, this.scoreDisplay);

        // touch enemies to lose health
        this.healthDisplay = new MetricDisplay(this, 16, 56, 'Health', 100);
        this.enemyGroup = new EnemyGroup(this, [
            { x: 400, y: 530, },
            { x: 750, y: 270, }
        ]);
        this.physics.add.collider(this.enemyGroup.group, tileLayer);
        this.damageOnTouch = new DamageOnTouch(this, this.player, this.enemyGroup.group, this.healthDisplay, 10);
        this.gameOverMonitor = new GameOverOnHealth(this, this.healthDisplay);


        // fire bullets to kill enemies and award scores
        this.bulletGroup = new BulletGroup(this);
        this.shooter     = new Shooter(this, this.player, this.bulletGroup, 'F');
        this.physics.add.collider(this.bulletGroup, tileLayer,
                                  b => b.disableBody(true, true));
        this.bulletEnemyCollision = new BulletEnemyCollision(
            this,
            this.bulletGroup,
            this.enemyGroup.group,
            this.scoreDisplay,  // give it your score display
            10                  // scores per kill
        );

        // create the chaser enemy
        this.chaser = new ChasingEnemy(this, 200, 100, 'enemy_idle', 'enemy_run', this.player, 60);
        this.physics.add.collider(this.chaser, tileLayer);
        this.chaserDamage = new DamageOnTouch(
            this, 
            this.player, 
            this.chaser,       // single sprite works here too
            this.healthDisplay,
            10
        );
        this.physics.add.overlap(
            this.bulletGroup, 
            this.chaser,
            (bullet, chaser) => {
                bullet.disableBody(true, true);
                chaser.disableBody(true, true);
                this.scoreDisplay.add(10);
            }
        );

        // eat apples to gain immunity for a while
        this.appleGroup = new AppleGroup(this, [
            { x: 200, y: 200, key: 'apple' },
            { x: 600, y: 360, key: 'apple' }
        ]);
        this.immunityDisplay = new MetricDisplay(this, 16, 96, 'Immunity', 0);
        this.immunityPowerUp = new ImmunityPowerUp(
            this,
            this.player,
            this.appleGroup.group,
            this.immunityDisplay,
            15000
        );

        // Reach the flag to win
        this.destination = new Destination(this, this.player, 1500, 500, 'flag');
        this.physics.add.collider(this.destination.sprite, tileLayer);
        this.physics.add.overlap(this.player, this.destination.sprite, () => {
            this.destination.onReach();
        });
        
        // Create fire and jump buttons
        controlPanel.setButtons(
            ['Fire', 'Jump'],
            [() => this.shooter.fire(), () => this.player.jump()]
        );

        // --- End of customizable section ---
    }

    update() {
        this.player.update();
        this.shooter.update();
        if (this.chaser) this.chaser.update();
        this.gameOverMonitor.update();
    }
    restart() {
        this.scene.restart();
    }
}



