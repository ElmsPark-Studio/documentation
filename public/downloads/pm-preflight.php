<?php
/**
 * ElmsPark Preflight for PageMotor
 * ---------------------------------
 * A single-file, read-only host check you run BEFORE installing PageMotor.
 *
 * Upload this file into the folder where PageMotor will live, open it in a
 * browser, read the report, then delete it. It answers, in plain English,
 * whether this host can run PageMotor at all, and names the fix for anything
 * that would stop it.
 *
 * Deliberate constraints, all of which matter:
 *
 *   1. PHP 5.2-era SYNTAX ONLY. This tool's single most important job is
 *      telling someone their PHP is too old. A tool written in modern PHP
 *      would itself fail to parse on old PHP and render a blank white page,
 *      which is the exact symptom it is supposed to explain. So: no ??, no
 *      scalar type hints, no return types, no arrow functions, no match, no
 *      str_contains, no ::class, no spread. It must run anywhere.
 *   2. Never fatal. Every probe is wrapped. A disabled function, a blocked
 *      socket or an unreadable directory is a FINDING to report, not a crash.
 *   3. No credentials, ever. It never asks for a database password and has no
 *      form to type one into. It reads the host, nothing else.
 *   4. No outbound assets. No web fonts, no CDN. It must render identically on
 *      a host with no outbound network access.
 *   5. Read-only, bar one write test that cleans up after itself.
 *
 * Part of the ElmsPark guides: https://documentation.elmspark.com/guides/
 */

@error_reporting(E_ALL);
@ini_set('display_errors', '0');   // our report IS the output; a raw notice would only confuse
@set_time_limit(60);

define('PF_VERSION', '1.0.0');

/* ------------------------------------------------------------------ *
 * Helpers. PHP 5.2-safe throughout.
 * ------------------------------------------------------------------ */

/**
 * status: 'ok' | 'warn' | 'fail' | 'info'
 */
function pf_row($label, $status, $detail, $fix) {
	return array(
		'label'  => $label,
		'status' => $status,
		'detail' => $detail,
		'fix'    => $fix
	);
}

function pf_e($s) {
	return htmlspecialchars($s, ENT_QUOTES, 'UTF-8');
}

function pf_bytes_to_int($val) {
	$val = trim($val);
	if ($val === '') { return 0; }
	$last = strtolower(substr($val, -1));
	$num  = (float) $val;
	if ($last === 'g') { $num = $num * 1024 * 1024 * 1024; }
	else if ($last === 'm') { $num = $num * 1024 * 1024; }
	else if ($last === 'k') { $num = $num * 1024; }
	return (int) $num;
}

function pf_here() {
	return dirname(__FILE__);
}

/* ------------------------------------------------------------------ *
 * Probes
 * ------------------------------------------------------------------ */

$rows_core   = array();
$rows_files  = array();
$rows_limits = array();
$rows_net    = array();
$rows_ctx    = array();

/* --- 1. PHP version. The headline check. --- */

$php = PHP_VERSION;
if (version_compare($php, '8.0', '<')) {
	$rows_core[] = pf_row(
		'PHP version',
		'fail',
		'This server is running PHP ' . $php . '. PageMotor needs PHP 8. On PHP 7 or older it will not run at all, and the usual symptom is a completely blank white page with no error message.',
		'In cPanel, open Software, then MultiPHP Manager. Tick this domain, choose PHP 8.2 or newer from the dropdown, and click Apply. Then reload this page. If your host has no such panel, ask them to move this domain to PHP 8.'
	);
} else if (version_compare($php, '8.2', '<')) {
	$rows_core[] = pf_row(
		'PHP version',
		'warn',
		'This server is running PHP ' . $php . '. PageMotor will run, but this version no longer receives security updates from the PHP project itself.',
		'Worth moving to PHP 8.2 or newer when convenient: cPanel, then Software, then MultiPHP Manager. Not urgent, and it will not stop the install.'
	);
} else {
	$rows_core[] = pf_row(
		'PHP version',
		'ok',
		'PHP ' . $php . '. Modern and supported.',
		''
	);
}

/* --- 2. Extensions --- */

$ext_essential = array(
	'mysqli'   => 'talking to your database. Without it PageMotor cannot store or read a single page.',
	'json'     => 'reading and writing structured data. Core to almost everything PageMotor does.',
	'mbstring' => 'handling accented characters and non-English text correctly.'
);
$ext_important = array(
	'curl'     => 'fetching plugin updates and connecting to outside services.',
	'openssl'  => 'making secure HTTPS connections out from your server.',
	'fileinfo' => 'working out what an uploaded file actually is, which matters for safe uploads.'
);
$ext_optional = array(
	'zip'      => 'installing plugins and themes from a zip file inside the admin.',
	'intl'     => 'formatting dates and numbers for other regions.'
);

$missing_essential = array();
foreach ($ext_essential as $name => $why) {
	if (!extension_loaded($name)) { $missing_essential[] = $name; }
}
if (count($missing_essential) > 0) {
	$detail = 'Missing: ' . implode(', ', $missing_essential) . '. ';
	foreach ($missing_essential as $name) {
		$detail .= $name . ' handles ' . $ext_essential[$name] . ' ';
	}
	$rows_core[] = pf_row('Essential PHP extensions', 'fail', trim($detail),
		'These are not optional. In cPanel look for "Select PHP Version" or MultiPHP INI Editor and enable them, or ask your host to. Most hosts have them on by default, so if one is missing it is usually a single tick box.');
} else {
	$rows_core[] = pf_row('Essential PHP extensions', 'ok', 'mysqli, json and mbstring are all present.', '');
}

$missing_important = array();
foreach ($ext_important as $name => $why) {
	if (!extension_loaded($name)) { $missing_important[] = $name; }
}
if (count($missing_important) > 0) {
	$detail = 'Missing: ' . implode(', ', $missing_important) . '. ';
	foreach ($missing_important as $name) {
		$detail .= $name . ' handles ' . $ext_important[$name] . ' ';
	}
	$rows_core[] = pf_row('Recommended PHP extensions', 'warn', trim($detail),
		'PageMotor will install without these, but plugin updates and outbound connections may not work. Same place as above: "Select PHP Version" in cPanel, or ask your host.');
} else {
	$rows_core[] = pf_row('Recommended PHP extensions', 'ok', 'curl, openssl and fileinfo are all present.', '');
}

/* images: gd OR imagick is enough */
if (extension_loaded('gd') || extension_loaded('imagick')) {
	$which = extension_loaded('gd') ? 'gd' : 'imagick';
	$rows_core[] = pf_row('Image handling', 'ok', 'Present (' . $which . '). Image resizing will work.', '');
} else {
	$rows_core[] = pf_row('Image handling', 'warn',
		'Neither gd nor imagick is available, so PageMotor cannot resize images. Uploads will still work, but every image will be served at its original size.',
		'Enable gd in cPanel under "Select PHP Version", or ask your host to. gd is the more commonly available of the two.');
}

$missing_optional = array();
foreach ($ext_optional as $name => $why) {
	if (!extension_loaded($name)) { $missing_optional[] = $name; }
}
if (count($missing_optional) > 0) {
	$rows_core[] = pf_row('Optional extras', 'info',
		'Not present: ' . implode(', ', $missing_optional) . '. Nothing here blocks an install.', '');
}

/* --- 3. Disabled functions --- */

$disabled_raw = @ini_get('disable_functions');
if ($disabled_raw === false) { $disabled_raw = ''; }
$disabled = array();
if (trim($disabled_raw) !== '') {
	$parts = preg_split('/[\s,]+/', $disabled_raw);
	foreach ($parts as $p) {
		$p = trim($p);
		if ($p !== '') { $disabled[] = strtolower($p); }
	}
}
$needed = array('file_get_contents', 'file_put_contents', 'fopen', 'fwrite', 'unlink', 'mkdir');
$blocked = array();
foreach ($needed as $fn) {
	if (in_array(strtolower($fn), $disabled)) { $blocked[] = $fn; }
}
if (count($blocked) > 0) {
	$rows_core[] = pf_row('Blocked PHP functions', 'fail',
		'Your host has disabled functions PageMotor needs: ' . implode(', ', $blocked) . '.',
		'This is a hosting policy, not something you can change from cPanel. Contact your host, quote the function names above, and ask whether they can be enabled for your account. If they refuse, this host cannot run PageMotor.');
} else if (count($disabled) > 0) {
	$rows_core[] = pf_row('Blocked PHP functions', 'ok',
		'Your host disables ' . count($disabled) . ' function(s), but none that PageMotor depends on.', '');
} else {
	$rows_core[] = pf_row('Blocked PHP functions', 'ok', 'Nothing relevant is blocked.', '');
}

/* --- 4. Can PHP write here? The install wizard must create config.php. --- */

$here      = pf_here();
$probe     = $here . DIRECTORY_SEPARATOR . '.pm-preflight-write-test.tmp';
$wrote     = false;
$write_err = '';
$fh = @fopen($probe, 'wb');
if ($fh) {
	if (@fwrite($fh, 'preflight') !== false) { $wrote = true; }
	@fclose($fh);
	@unlink($probe);
} else {
	$write_err = 'could not create a file';
}
if ($wrote) {
	$rows_files[] = pf_row('Writing files in this folder', 'ok',
		'PHP can create and delete files here. The install wizard will be able to write config.php for you.', '');
} else {
	$rows_files[] = pf_row('Writing files in this folder', 'fail',
		'PHP cannot write into this folder (' . $write_err . '). The install wizard will not be able to create config.php, and uploads will fail later.',
		'In cPanel File Manager, select this folder, click Permissions, and set it to 755. If that does not help, the folder is probably owned by the wrong user and your host needs to fix the ownership.');
}

/* --- 5. Are the PageMotor files actually here? --- */

$has_core   = @file_exists($here . DIRECTORY_SEPARATOR . 'pagemotor.php');
$has_sample = @file_exists($here . DIRECTORY_SEPARATOR . 'config-sample.php');
$has_config = @file_exists($here . DIRECTORY_SEPARATOR . 'config.php');

/* the classic trap: the zip extracted into a subfolder */
$nested = array();
$entries = @scandir($here);
if (is_array($entries)) {
	foreach ($entries as $entry) {
		if ($entry === '.' || $entry === '..') { continue; }
		$path = $here . DIRECTORY_SEPARATOR . $entry;
		if (@is_dir($path) && @file_exists($path . DIRECTORY_SEPARATOR . 'pagemotor.php')) {
			$nested[] = $entry;
		}
	}
}

if ($has_core) {
	$msg = 'pagemotor.php is here, so the files are in the right place.';
	if ($has_config) {
		$msg .= ' config.php already exists, so this install has been configured.';
	} else if ($has_sample) {
		$msg .= ' config.php does not exist yet, which is normal before you install. config-sample.php is present to copy from if you prefer the hand-edit route.';
	} else {
		$msg .= ' Neither config.php nor config-sample.php is here, which is unusual.';
	}
	$rows_files[] = pf_row('PageMotor files', 'ok', $msg, '');
} else if (count($nested) > 0) {
	$rows_files[] = pf_row('PageMotor files', 'fail',
		'PageMotor is not in this folder, it is one level down inside "' . implode('", "', $nested) . '". This happens when the zip extracts into a folder of its own. Your site will not load until the files sit here, alongside this check.',
		'In cPanel File Manager, open "' . $nested[0] . '", click Select All, then Move, and move everything up one level into this folder. Then delete the now-empty folder and reload this page.');
} else {
	$rows_files[] = pf_row('PageMotor files', 'info',
		'No PageMotor files here yet. That is fine if you have not uploaded them, this check works perfectly well on an empty folder.',
		'');
}

/* --- 6. Limits --- */

$mem_raw = @ini_get('memory_limit');
if ($mem_raw === false) { $mem_raw = ''; }
$mem = pf_bytes_to_int($mem_raw);
if ($mem_raw === '-1' || $mem === 0) {
	$rows_limits[] = pf_row('Memory limit', 'ok', 'No limit set by PHP.', '');
} else if ($mem < 128 * 1024 * 1024) {
	$rows_limits[] = pf_row('Memory limit', 'warn',
		'Set to ' . $mem_raw . '. PageMotor runs comfortably at 128M and above. Below that you may hit blank pages on image-heavy admin screens.',
		'In cPanel, MultiPHP INI Editor, set memory_limit to 256M. If the setting will not stick, your host has capped it and you would need to ask them.');
} else {
	$rows_limits[] = pf_row('Memory limit', 'ok', 'Set to ' . $mem_raw . '. Plenty.', '');
}

$maxex = @ini_get('max_execution_time');
$maxex_i = (int) $maxex;
if ($maxex_i === 0) {
	$rows_limits[] = pf_row('Script time limit', 'ok', 'No limit.', '');
} else if ($maxex_i < 30) {
	$rows_limits[] = pf_row('Script time limit', 'warn',
		'Set to ' . $maxex_i . ' seconds. Long jobs such as an import or a bulk image resize may be cut off partway.',
		'MultiPHP INI Editor, set max_execution_time to 120.');
} else {
	$rows_limits[] = pf_row('Script time limit', 'ok', $maxex_i . ' seconds.', '');
}

$upl_raw  = @ini_get('upload_max_filesize');
$post_raw = @ini_get('post_max_size');
if ($upl_raw === false) { $upl_raw = ''; }
if ($post_raw === false) { $post_raw = ''; }
$upl  = pf_bytes_to_int($upl_raw);
$post = pf_bytes_to_int($post_raw);
if ($upl > 0 && $upl < 8 * 1024 * 1024) {
	$rows_limits[] = pf_row('Upload size limit', 'warn',
		'Uploads are capped at ' . $upl_raw . '. Larger images and plugin zips will be refused.',
		'MultiPHP INI Editor, set upload_max_filesize to 64M and post_max_size to 64M as well.');
} else if ($post > 0 && $upl > 0 && $post < $upl) {
	$rows_limits[] = pf_row('Upload size limit', 'warn',
		'upload_max_filesize is ' . $upl_raw . ' but post_max_size is only ' . $post_raw . '. The smaller of the two wins, so your real limit is ' . $post_raw . '.',
		'MultiPHP INI Editor, set post_max_size to at least match upload_max_filesize.');
} else {
	$rows_limits[] = pf_row('Upload size limit', 'ok',
		'Uploads up to ' . ($upl_raw !== '' ? $upl_raw : 'the host default') . '.', '');
}

/* --- 7. Outbound HTTPS. PageMotor needs this for updates. --- */

$target = 'https://updates.elmspark.com/';
$out_ok = false;
$out_note = '';
if (function_exists('curl_init')) {
	$ch = @curl_init($target);
	if ($ch) {
		@curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
		@curl_setopt($ch, CURLOPT_NOBODY, true);
		@curl_setopt($ch, CURLOPT_TIMEOUT, 8);
		@curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 5);
		@curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true);
		@curl_exec($ch);
		$code = (int) @curl_getinfo($ch, CURLINFO_HTTP_CODE);
		$cerr = @curl_error($ch);
		@curl_close($ch);
		/* Any reply at all proves the connection worked. The status code itself is
		   irrelevant here and showing it only alarms people, so it stays internal. */
		if ($code > 0) { $out_ok = true; $out_note = 'The update server replied.'; }
		else { $out_note = $cerr !== '' ? $cerr : 'no response'; }
	} else {
		$out_note = 'curl could not start';
	}
} else if (@ini_get('allow_url_fopen')) {
	$ctx = @stream_context_create(array('http' => array('timeout' => 8, 'method' => 'HEAD')));
	$fp  = @fopen($target, 'r', false, $ctx);
	if ($fp) { $out_ok = true; $out_note = 'reached via fopen.'; @fclose($fp); }
	else { $out_note = 'fopen could not connect'; }
} else {
	$out_note = 'neither curl nor allow_url_fopen is available';
}

if ($out_ok) {
	$rows_net[] = pf_row('Outbound HTTPS', 'ok',
		'This server can reach the outside world. ' . $out_note . ' Plugin updates and licence checks will work.', '');
} else {
	$rows_net[] = pf_row('Outbound HTTPS', 'warn',
		'This server could not make an outbound HTTPS request (' . $out_note . '). PageMotor will install and run, but it will not be able to check for plugin updates.',
		'Some shared hosts block outbound connections by default. Ask your host to allow outbound HTTPS on port 443, quoting that your application needs to reach external update servers.');
}

/* --- 8. Context. Answers "am I even in the right folder?" --- */

$sapi = php_sapi_name();
$srv  = isset($_SERVER['SERVER_SOFTWARE']) ? $_SERVER['SERVER_SOFTWARE'] : 'unknown';
$docroot = isset($_SERVER['DOCUMENT_ROOT']) ? $_SERVER['DOCUMENT_ROOT'] : '';
$here_real = @realpath($here);
$doc_real  = $docroot !== '' ? @realpath($docroot) : '';

$rows_ctx[] = pf_row('This folder', 'info', $here_real ? $here_real : $here, '');
if ($doc_real && $here_real && $doc_real === $here_real) {
	$rows_ctx[] = pf_row('Document root', 'ok',
		'This folder IS the document root for the address you used. PageMotor installed here will be served at the top level of this domain.', '');
} else if ($doc_real) {
	$rows_ctx[] = pf_row('Document root', 'warn',
		'The document root for this address is ' . $doc_real . ', which is not the folder this file is in. PageMotor installed here would appear in a subfolder of the site rather than at its root.',
		'If you meant this domain to serve from here, correct its Document Root in cPanel under Domains. If you deliberately put this file in a subfolder, ignore this.');
}
$rows_ctx[] = pf_row('Server', 'info', $srv . ' (PHP running as ' . $sapi . ')', '');

if (function_exists('apache_get_modules')) {
	$mods = @apache_get_modules();
	if (is_array($mods) && in_array('mod_rewrite', $mods)) {
		$rows_ctx[] = pf_row('URL rewriting', 'ok', 'mod_rewrite is enabled, so tidy page addresses will work.', '');
	} else if (is_array($mods)) {
		$rows_ctx[] = pf_row('URL rewriting', 'warn',
			'mod_rewrite does not appear to be enabled. Without it every page address needs index.php in it.',
			'Ask your host to enable mod_rewrite. On cPanel hosting it is almost always on, so this may just be undetectable from here.');
	}
} else {
	$rows_ctx[] = pf_row('URL rewriting', 'info',
		'Cannot be detected from this setup. That is normal and not a problem; it simply means PHP is not running as an Apache module here.', '');
}

/* ------------------------------------------------------------------ *
 * Tally
 * ------------------------------------------------------------------ */

$all = array_merge($rows_core, $rows_files, $rows_limits, $rows_net, $rows_ctx);
$n_fail = 0; $n_warn = 0;
foreach ($all as $r) {
	if ($r['status'] === 'fail') { $n_fail++; }
	else if ($r['status'] === 'warn') { $n_warn++; }
}

if ($n_fail > 0) {
	$verdict_class = 'bad';
	$verdict_head  = $n_fail === 1 ? 'One thing will stop PageMotor installing' : $n_fail . ' things will stop PageMotor installing';
	$verdict_sub   = 'Fix the red items below, then reload this page. Everything red has a fix written under it.';
} else if ($n_warn > 0) {
	$verdict_class = 'okish';
	$verdict_head  = 'This host can run PageMotor';
	$verdict_sub   = $n_warn === 1
		? 'One thing is worth tidying up, but nothing here blocks the install. Carry on.'
		: $n_warn . ' things are worth tidying up, but nothing here blocks the install. Carry on.';
} else {
	$verdict_class = 'good';
	$verdict_head  = 'This host is ready for PageMotor';
	$verdict_sub   = 'Every check passed. Delete this file and start the install.';
}

function pf_render($title, $rows) {
	if (count($rows) === 0) { return; }
	echo '<h2>' . pf_e($title) . '</h2>';
	foreach ($rows as $r) {
		echo '<div class="row ' . pf_e($r['status']) . '">';
		echo '<div class="dot"></div>';
		echo '<div class="body">';
		echo '<h3>' . pf_e($r['label']) . '</h3>';
		echo '<p>' . pf_e($r['detail']) . '</p>';
		if ($r['fix'] !== '') {
			echo '<p class="fix"><strong>Fix:</strong> ' . pf_e($r['fix']) . '</p>';
		}
		echo '</div></div>';
	}
}
?><!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>PageMotor Preflight</title>
<style>
:root{
  --paper:#f7f3ea; --card:#fffdf8; --ink:#23211c; --soft:#5d574c;
  --pine:#2f5d4a; --pine-deep:#234a3b; --line:#e4ddcd;
  --accent:#c97a3c; --warn:#9a4b2e; --good:#2f6d4f;
}
*{box-sizing:border-box}
body{
  margin:0; background:var(--paper); color:var(--ink);
  font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
  line-height:1.6; font-size:17px;
}
.wrap{max-width:760px; margin:0 auto; padding:32px 20px 72px}
h1{font-size:30px; line-height:1.2; margin:0 0 4px; color:var(--pine-deep); letter-spacing:-.01em}
.lede{color:var(--soft); margin:0 0 26px; font-size:16px}
.verdict{border-radius:14px; padding:20px 22px; margin:0 0 30px; border:1px solid var(--line); background:var(--card)}
.verdict h2{margin:0 0 6px; font-size:21px; border:0; padding:0}
.verdict p{margin:0; color:var(--soft); font-size:15.5px}
.verdict.good{border-left:5px solid var(--good)}
.verdict.good h2{color:var(--good)}
.verdict.okish{border-left:5px solid var(--accent)}
.verdict.okish h2{color:var(--accent)}
.verdict.bad{border-left:5px solid var(--warn)}
.verdict.bad h2{color:var(--warn)}
h2{font-size:14px; text-transform:uppercase; letter-spacing:.09em; color:var(--soft);
   margin:34px 0 12px; padding-bottom:7px; border-bottom:1px solid var(--line); font-weight:600}
.row{display:flex; gap:13px; align-items:flex-start; background:var(--card);
     border:1px solid var(--line); border-radius:12px; padding:15px 17px; margin:0 0 10px}
.dot{width:11px; height:11px; border-radius:50%; flex:0 0 11px; margin-top:8px}
.row.ok   .dot{background:var(--good)}
.row.warn .dot{background:var(--accent)}
.row.fail .dot{background:var(--warn)}
.row.info .dot{background:#b5ab97}
.row.fail{border-color:#e8c9bd}
.body{min-width:0; flex:1}
.row h3{margin:0 0 3px; font-size:16.5px; font-weight:600}
.row p{margin:0; color:var(--soft); font-size:15px; overflow-wrap:break-word; word-wrap:break-word}
.row .fix{margin-top:8px; color:var(--ink); background:#f3efe4;
          border-radius:8px; padding:9px 12px; font-size:14.5px}
.cleanup{margin:34px 0 0; border-radius:12px; padding:16px 18px;
         background:#f3efe4; border:1px solid var(--line); font-size:15px}
.cleanup strong{color:var(--warn)}
footer{margin-top:30px; padding-top:18px; border-top:1px solid var(--line);
       color:var(--soft); font-size:13.5px}
footer a{color:var(--pine)}
@media (max-width:520px){ body{font-size:16px} h1{font-size:25px} .wrap{padding:22px 15px 60px} }
</style>
</head>
<body>
<div class="wrap">

  <h1>PageMotor Preflight</h1>
  <p class="lede">A read-only check of this host, run before installing PageMotor. Nothing here changes your server.</p>

  <div class="verdict <?php echo pf_e($verdict_class); ?>">
    <h2><?php echo pf_e($verdict_head); ?></h2>
    <p><?php echo pf_e($verdict_sub); ?></p>
  </div>

<?php
pf_render('Can this host run PageMotor', $rows_core);
pf_render('This folder', $rows_files);
pf_render('Limits', $rows_limits);
pf_render('Outside connections', $rows_net);
pf_render('Where you are', $rows_ctx);
?>

  <div class="cleanup">
    <strong>Delete this file when you are done.</strong>
    It holds no passwords and changes nothing, but it does describe your server's setup,
    and that is not information worth leaving on a public address. In cPanel File Manager,
    select <code>pm-preflight.php</code> and click Delete.
  </div>

  <footer>
    ElmsPark Preflight for PageMotor, version <?php echo pf_e(PF_VERSION); ?>.
    Guides and install walkthroughs: <a href="https://documentation.elmspark.com/guides/">documentation.elmspark.com/guides</a>
  </footer>

</div>
</body>
</html>
