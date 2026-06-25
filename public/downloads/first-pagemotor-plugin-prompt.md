# Building your first PageMotor plugin: interactive prompt

Paste everything below into Claude, ChatGPT, Gemini or any capable AI assistant. It will walk you through building the plugin one step at a time.

---

You are my setup assistant. Walk me through building my first PageMotor plugin, one step at a time, in British English. After each step, wait for me to confirm it worked before moving on. If I run into a problem, help me diagnose it before we continue. Keep each step short and give me the exact file contents to copy.

Use the material below. Do not paste it all at once. Lead me through it conversationally.

## What we are building

A minimal PageMotor plugin that registers one working shortcode, `[hello-world]`. The plugin lives in `user-content/plugins/my-hello-world/plugin.php`. It extends `PM_Plugin`, the framework base class, and uses the `shortcodes()` valet method to register the shortcode. No build tools, no Composer, no npm.

## Step 1: Make the folder and the header comment

Create the folder `user-content/plugins/my-hello-world/` inside the PageMotor install, then create `plugin.php` inside it. The file must start with a header comment that PageMotor reads to identify the plugin. Give the user this exact content for the top of `plugin.php`:

    <?php
    /*
    Name: My Hello World
    Author: Your Name
    Description: A minimal first plugin with one shortcode.
    Version: 1.0
    Requires: 0.9
    Class: My_Hello_World
    License: OpenAttribution
    */

Explain that `Class:` must match the PHP class name exactly. Tell them that PageMotor reads only the first 500 bytes of the file for the `Version:` header, so they should keep the header short and put `Version:` near the top.

## Step 2: Declare the plugin class

Directly below the header comment, add the class declaration. The class must extend `PM_Plugin`:

    class My_Hello_World extends PM_Plugin {

    }

Explain that this is already a complete, loadable plugin even though it does nothing yet. Mention that they can override `construct()` for early setup work (database tables, includes) and `init()` for work that depends on settings being available, but they must never override `__construct()` or `_init()`, which are framework-owned.

## Step 3: Add the shortcodes valet

Inside the class, add the `shortcodes()` valet method and the handler it points to:

    public function shortcodes() {
        return [
            'hello-world' => 'render_hello'
        ];
    }

    public function render_hello($args = []) {
        $name = !empty($args['name']) ? htmlspecialchars($args['name']) : 'world';
        return '<p>Hello, ' . $name . '!</p>';
    }

Explain that `shortcodes()` returns a map of shortcode tag names to method names on the class. The handler receives any shortcode attributes as `$args` and must return its HTML, not echo it.

Warn them: if the shortcode needs CSS, they must use `css_sitewide()` to register it, not `css()`. The `css()` method only fires when the plugin is placed in the current page template; shortcodes can appear on any page, so they need `css_sitewide()` to load everywhere.

## Step 4: Install and activate

Tell the user to go to the Plugins section in the PageMotor admin. Their plugin should appear in the list, identified by the `Name:` field. They need to click Install, then Activate. Warn them that a PHP syntax error in `plugin.php` will take the whole site down until the file is fixed, because PageMotor includes it directly. Encourage them to keep the file simple and test each change.

## Step 5: Test the shortcode on a page

Ask the user to edit any page in the PageMotor content editor and add this to the page body:

    [hello-world]

Save it, visit the page, and they should see "Hello, world!" Then try:

    [hello-world name="Kenn"]

That should give "Hello, Kenn!"

Remind them: shortcodes only run on pages with `type=page`. If they see the shortcode as plain text, check the page type in the content editor. A `type=html` page serves content verbatim without processing shortcodes.

## Common problems to watch for

If the plugin does not appear in the admin: check the folder is in `user-content/plugins/`, that `plugin.php` is inside it, and that the header comment is valid (opens with `/*`, closes with `*/`, has `Name:` and `Class:` fields).

If the site goes blank after activation: there is a PHP fatal error. Tell the user to rename the plugin folder temporarily to bring the site back, then fix the file.

If the shortcode appears as plain text: check the plugin is active and the page type is `page`, not `html`.

If CSS is not loading: confirm they are using `css_sitewide()` for shortcode styles, not `css()`.

## What to build next

Once the shortcode is working, offer to walk them through one of these natural next steps: adding a settings panel with `settings()`, adding an AJAX handler with `ajax()`, or loading a CSS file sitewide with `css_sitewide()`. Ask which they would like to try.
