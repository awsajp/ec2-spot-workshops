<!DOCTYPE html>
<html>
<head>
<title>README.md - Containers-immersionday-workshop - Code Browser</title>
<meta content='width=device-width, initial-scale=1' name='viewport'>
<meta content='true' name='use-sentry'>
<meta name='request-id'>
<meta name="csrf-param" content="authenticity_token" />
<meta name="csrf-token" content="IiyrCc6z+C7QSPr9MUxCb3QQrqIzyBu668eKoOKyL113/lt8/CGctUAW93OxVkZtnTbmJ9TRY8BKUldxLwSYLg==" />
<meta content='IE=edge' http-equiv='X-UA-Compatible'>

<link rel="shortcut icon" type="image/x-icon" href="https://internal-cdn.amazon.com/code.amazon.com/pub/assets/cdn/favicon-c8c77da180d3e9e679dac48d5ae77858edd6974d6a2a78b1705dc0b499c1d7c2.ico" />
<link rel="stylesheet" media="all" href="https://internal-cdn.amazon.com/oneg.amazon.com/assets/3.2.4/css/application.min.css" />
<link rel="stylesheet" media="all" href="https://internal-cdn.amazon.com/code.amazon.com/pub/assets/cdn/vendor-d474406fcd55deaf625f229972589710c6e60818248e2c7b50bd77c2f29bf015.css" />
<link rel="stylesheet" media="all" href="https://internal-cdn.amazon.com/code.amazon.com/pub/assets/cdn/application-oneg-5a911f5dfd4184c9faee1ac1aa4f678492378fa6c9b9fe35843d8e39e5cf4092.css" />
<link rel="stylesheet" media="all" href="https://internal-cdn.amazon.com/is-it-down.amazon.com/stylesheets/stripe.css" />
<style>
  /* line 1, (__TEMPLATE__) */
  .absolute-time {
    display: none; }
  
  /* line 3, (__TEMPLATE__) */
  .relative-time {
    display: auto; }
</style>
<style>
  /* line 1, (__TEMPLATE__) */
  .add_related_items {
    display: none; }
  
  /* line 3, (__TEMPLATE__) */
  #related_items {
    min-height: 75px; }
    /* line 5, (__TEMPLATE__) */
    #related_items .error {
      color: red; }
</style>
<link rel="stylesheet" media="screen" href="https://internal-cdn.amazon.com/code.amazon.com/pub/assets/cdn/spiffy_diffy_assets/spiffy_diffy-21a1a3240dcb4bd1500349e41c651a2065e7ff594ee849bbe7aa1b09227b8d39.css" />
<link rel="stylesheet" media="screen" href="https://internal-cdn.amazon.com/code.amazon.com/pub/assets/cdn/blobs-061e7f23bbbcb6304112ba461f3dfee236247167c4a1a6ca3e2e2ddc47ef3740.css" />

</head>
<body>
<nav class='navbar navbar-default hidden-print' role='navigation'>
<div class='container-fluid'>
<div class='navbar-header'>
<a class='navbar-brand' href='/'>Code Browser</a>
</div>
<ul class='nav navbar-nav'>
<li>
<div class='advanced-search-hover-link'>
<!-- / preserves query and redirects to advanced search -->
<a class="fa fa-magic" href="/search?&amp;commit=Search"></a>
</div>
<form action='/search' class='form-inline navbar-search navbar-form'>
<div class='search-spinner' style='display:none'>
<img src='https://images-na.ssl-images-amazon.com/images/G/01/oneg/img/spinner.gif'>
</div>
<div class='input-append inline-elem'>
<input accesskey='s' class='hinted input-medium autocomplete-packages search-query form-control search' data-autocomplete-url='/packages/autocomplete_package_id?vs=true' id='search_top' name='term' placeholder='Code Search' role='search' size='40' tabindex='1' title='Code Search' type='text'>
</div>
<a href='#'>
<img src='https://internal-cdn.amazon.com/btk.amazon.com/img/icons-1.0/tooltip-bubble.png' target_popup='search-bar-hint'>
</a>
<div class='popover fade right in code-search-help-box nav' id='search-bar-hint'>
<h3 class='popover-title'>Code Search Hints</h3>
<div class='popover-content'>
<p>
<strong class='external text'>
<a href='/search' rel='nofollow'>Advanced Search</a>
</strong>
</p>
<p>
<strong>Simple search:</strong>
&lt;term&gt;
</p>
<p>
<strong>Prefix search:</strong>
&lt;at-least-three-chars&gt;*
</p>
<p>
<strong>Find files with at least one of two terms:</strong>
&lt;term1&gt; &lt;term2&gt;
</p>
<p>
<strong>Find files with at least one of two terms but not a third term:</strong>
&lt;term1&gt; &lt;term2&gt;&nbsp;!&lt;term3&gt;
</p>
<p>
<strong>Find files with two terms in sequence:</strong>
"&lt;term1&gt; &lt;term2&gt;"
</p>
<p>
<strong>Filter to only one or more repository:</strong>
&lt;term1&gt; rp:&lt;MyPackageName&gt; ...
</p>
<p>
<strong>Filter to a particular file extension:</strong>
&lt;term1&gt; path:.java
</p>
<p>
<strong>Filter out a particular file extension (works w/ all filters):</strong>
&lt;term1&gt; path:!.java
</p>
<p>
<strong>Filter to a path: &lt;term1&gt;</strong>
path:/my/path/to/consider*
</p>
<p>
<strong>Filter by write permissions:</strong>
group:&lt;some-ldap-posix-or-source-group&gt;
</p>
<p>
<strong>Filter by package status:</strong>
status:active:deprecated
</p>
<p>
<strong>Filter by branch: branch:&lt;branch-name&gt;</strong>
</p>
<p>
<strong>Filter by third party:</strong>
third_party:true|false
</p>
<p>
<strong>Filter by particular class in java files:</strong>
class:&lt;class_name&gt;
</p>
<p>
<strong>Filter by method declarations in java files:</strong>
method:&lt;method_name&gt;
</p>
<p>
<strong>Filter by method calls in java files:</strong>
method_call:&lt;method_name&gt;
</p>
<p>
<strong>Filter by interface declarations in java files:</strong>
interface:&lt;interface_name&gt;
</p>
<p>
<a class='external text' href='https://w.amazon.com/index.php/BuilderTools/Product/CodeSearch/User%20Guide' rel='nofollow'>Read more here</a>
</p>
<p>
<i>(click on the speech bubble to close)</i>
</p>
</div>
</div>

</form>
</li>
<li>
<a href="/permissions">Permissions</a>
</li>
<li>
<a href="/workspaces/jalawala">Workspaces</a>
</li>
<li>
<a href="/version-sets">Version Sets</a>
</li>
<li>
<a data-target='#preferences_dialog' data-toggle='modal' id='preferences'>Preferences</a>
<div class='modal fade' id='preferences_dialog' role='dialog'>
<div class='modal-dialog modal-md'>
<div class='modal-content'>
<div class='modal-header'>
<button class='close' data-dismiss='modal' type='button'>
<i class='fa fa-times'></i>
</button>
<h4 class='modal-title'>User Preferences</h4>
</div>
<div class='modal-body'>
<div class='text-center'>
<i class='fa fa-spinner fa-spin'></i>
</div>
</div>
</div>
</div>
</div>
</li>
</ul>
<ul class='nav navbar-nav navbar-right'>
<li><a target="_blank" onclick="window.open('http://tiny/submit/url?opaque=1&name=' + encodeURIComponent(location.href)); return false;" href="#">Tiny Link <i class="fa fa-external-link"></i></a></li>
</ul>
</div>
</nav>

<div class='container-fluid'>
<ol class='breadcrumb'>
<li>
<a href="/">Home</a>
</li>
<li><a href="/packages/Containers-immersionday-workshop">Containers-immersionday-workshop</a></li>
<li><a href="/packages/Containers-immersionday-workshop/trees/mainline/--/">mainline</a></li>
<li class='.active'>README.md</li>


</ol>
<div id='content'>
</div>

<div class='page-header'>
<h1>
<span>
Containers-immersionday-workshop
</span>
<div class='star' data-package='Containers-immersionday-workshop'></div>
<small class='hidden-print'>
<a class='powertip autoselect pull-right' data-powertip='brazil ws use -p Containers-immersionday-workshop' id='bw_use'>
<i class='glyphicon glyphicon-download-alt'></i>
</a>
</small>
<small>
<span class='clone subtext pull-right hidden-print'>
<form class='form-inline'>
Clone uri:
<input class='form-control input-sm' type='text' value='ssh://git.amazon.com/pkg/Containers-immersionday-workshop'>
</form>
</span>

</small>
<small>
<div class='pull-right hidden-print' id='code_search_box'>
<form class="form-inline" action="/search_redirector" accept-charset="UTF-8" method="get"><input name="utf8" type="hidden" value="&#x2713;" />
<div class='input-group search '><input type="text" name="search_term" id="search_term" placeholder="Search in this package" size="21" class="form-control input-sm" />
<span class='input-group-btn'><button class='btn' type='submit'>Go</button></span></div><input type="hidden" name="package" id="package" value="Containers-immersionday-workshop" />
<input type="hidden" name="path" id="path" value="README.md" />
</form>

</div>

</small>
</h1>
<div class='badges'>
<div class='placeholder'>
&nbsp
</div>
<span id='third_party' style='display: none;'>
<span class='label label-info'>Third Party Package</span>
</span>
<div class='popover fade right in badge-helper-box' id='badge-hints'>
<h3 class='popover-title'>Hint</h3>
<div class='badge-helper-content popover-content'>
<p>
Package badge data is extracted from brazil metadata about a package.  Particularly, Code Browser finds the highest major version and fetches data about that package version from the latest build in the primary version set.
</p>
<p>
The metadata we have is based on following brazil conventions about where to place documentation and unit test (and coverage) output.  Here are a few other wiki pages that have more detailed information about these topics.
</p>
<ul>
<li>
Each
<a class='external text' href='https://w.amazon.com/index.php/BrazilBuildSystem/BuildSystems' rel='nofollow'>build system</a>
may have ways to configure build artifacts that the Brazil system recognizes.
</li>
<li>
Java - if you use
<a class='external text' href='https://w.amazon.com/index.php/BrazilBuildSystem/HappierTrails' rel='nofollow'>Happier Trails</a>
you should get test, documentation, and coverage data out of the box.
</li>
<li>
This
<a class='external text' href='https://w.amazon.com/index.php/BrazilBuildSystem/Concepts/UnitTestingInBrazil/JavaUnitTesting' rel='nofollow'>Java Unit Testing</a>
page describes the basic conventions underlying test output.  Most any language / build system can output usable information just by putting the right files in the right places.
</li>
</ul>
<p>
Here are some example packages for a few languages that are configured to expose this information to Brazil:
</p>
<ul>
<li>
Java -
<a class='external text' href='https://code.amazon.com/packages/ToolsPermsService/blobs/mainline/--/build.xml' rel='nofollow'>ToolsPermsService</a>
</li>
<li>
Ruby -
<a class='external text' href='https://code.amazon.com/packages/CriticService/blobs/mainline/--/Rakefile' rel='nofollow'>CriticService</a>
(
<a class='external text' href='https://w.amazon.com/index.php/BuilderTools/Product/BrazilRake' rel='nofollow'>BrazilRake's</a>
SimpleCov does most of the work)
</li>
<li>
Python -
<a class='external text' href='https://code.amazon.com/packages/Ducky/blobs/62906a55e2c53e9dc779a00770b39b0620d74c45/--/Config#line-48' rel='nofollow'>Ducky</a>
</li>
<li>
Perl - ?
</li>
</ul>
</div>
</div>

</div>
</div>
<div class='row'>
<div class='col-md-9'>
<ul class='nav nav-pills bottom-buffer-small hidden-print'>
<li class='active'><a href="/packages/Containers-immersionday-workshop">Source</a></li>
<li><a href="/packages/Containers-immersionday-workshop/logs">Commits</a></li>
<li><a href="/packages/Containers-immersionday-workshop/releases">Releases</a></li>
<li><a href="/packages/Containers-immersionday-workshop/metrics/c561dea942838bc0e25029134936a482af94a5da">Metrics</a></li>
<li><a href="/packages/Containers-immersionday-workshop/permissions">Permissions</a></li>
<li><a href="/gc/rules/for-package/Containers-immersionday-workshop">CRUX Rules</a></li>
<li><a href="/packages/Containers-immersionday-workshop/repo-info">Repository Info</a></li>
<li><a href="/packages/Containers-immersionday-workshop/replicas">CodeCommit Replicas</a></li>
</ul>

</div>
<div class='col-md-3'>
<div id='branch_and_search_box'>
<div class='hidden-print' id='branch_dropdown'>
<label for="branches">Branches: </label>
<input id='branches' name='branches' type='hidden'>
</div>

</div>

</div>
</div>
<div class='last_commit panel panel-default top-buffer-small'>
<div class='last_commit_heading'>
Last Commit
<span class='subtext'>
(<a class="commit-see-more" href="#">see more</a>)
</span>
</div>
<div class='panel-body'>
<ul class='last-commit-summary list-unstyled list-inline'>
<li class='commiter'></li>
<a href="https://code.amazon.com/users/beaumonm/activity">Mitch</a>
<li class='time'></li>
<span title='Committed on July 08, 2020 12:19:04 AM PDT' class='relative-time hover_tooltip year_old'>3 months ago</span><span class='absolute-time hover_tooltip year_old'>2020-07-08 00:19:04 PDT</span>
<li class='commit_message'>
<span class='refs'>
</span>
<a class='powertip commit black' data-commit-id='c561dea942838bc0e25029134936a482af94a5da' href='/packages/Containers-immersionday-workshop/commits/c561dea942838bc0e25029134936a482af94a5da'>
first commit
</a>
</li>
<li><a class="mono powertip autoselect" data-powertip="c561dea942838bc0e25029134936a482af94a5da" href="/packages/Containers-immersionday-workshop/commits/c561dea942838bc0e25029134936a482af94a5da#README.md">c561dea9</a></li>
<li>
<img src="https://pipelines.amazon.com/favicon.ico" alt="Favicon" />
<a href="https://pipelines.amazon.com/changes/PKG/Containers-immersionday-workshop/mainline/GitFarm:c561dea942838bc0e25029134936a482af94a5da">Track in pipelines</a>
</li>
</ul>

<div class='swappable-with-brief-header'>
<div class='commit_header'>
<div class='portrait'><a href="https://code.amazon.com/users/beaumonm/activity"><img class="" width="50" onerror="this.onerror=null; this.src=&#39;https://internal-cdn.amazon.com/code.amazon.com/pub/assets/cdn/default-user-b916c01d82910755cdba17db81688d35c994cf77a5907d721a6d93522961d007.gif&#39;" src="https://internal-cdn.amazon.com/badgephotos.amazon.com/phone-image.pl?uid=beaumonm" alt="Phone image" /></a></div>
<div class='details'>
<div class='pull-right' id='track_pipeline_change' style='clear-right'>
<ul class='list-unstyled'>
<li>
<img src="https://pipelines.amazon.com/favicon.ico" alt="Favicon" />
<a href="https://pipelines.amazon.com/changes/PKG/Containers-immersionday-workshop/mainline/GitFarm:c561dea942838bc0e25029134936a482af94a5da">Track in pipelines</a>
<span class='subtext'>(mainline)</span>
</li>
</ul>
</div>
<div class='download-diff pull-right' style='clear: right'>
<a href="/api/packages/Containers-immersionday-workshop/diff/c561dea942838bc0e25029134936a482af94a5da">Download Diff</a>
</div>
<div class='pull-right' id='browse_source' style='clear: right'>
<a href="/packages/Containers-immersionday-workshop/trees/c561dea942838bc0e25029134936a482af94a5da">Browse source at this commit</a>
</div>
<div class='pull-right' id='child_link' style='clear: right'>
<a href="/packages/Containers-immersionday-workshop/commits/c561dea942838bc0e25029134936a482af94a5da.child">view child commit</a>
</div>
<ul class='list-unstyled pull-right' style='clear: right'>
</ul>
<div class='author'>
<span class='name'><a href="https://code.amazon.com/users/beaumonm/activity">Mitch</a></span>
<span class='sha1'>
(<a class='powertip autoselect' data-powertip='c561dea942838bc0e25029134936a482af94a5da' href='/packages/Containers-immersionday-workshop/commits/c561dea942838bc0e25029134936a482af94a5da'>c561dea9</a>)
</span>
<div class='subtext'>
authored: <span title='July 08, 2020 12:19:04 AM PDT' class='relative-time hover_tooltip year_old'>3 months ago</span><span class='absolute-time hover_tooltip year_old'>2020-07-08 00:19:04 PDT</span>, committed: <span title='July 08, 2020 12:19:04 AM PDT' class='relative-time hover_tooltip year_old'>3 months ago</span><span class='absolute-time hover_tooltip year_old'>2020-07-08 00:19:04 PDT</span>
<div class='summaries'>
<div class='summary'>
Pushed to
<span class='autoselect branch powertip ref' data-powertip='mainline'>mainline</span>
by beaumonm <span title='September 14, 2020 10:52:41 PM PDT' class='relative-time hover_tooltip month_old'>17 days ago</span><span class='absolute-time hover_tooltip month_old'>2020-09-14 22:52:41 PDT</span> as part of <a class='powertip autoselect' data-powertip='7ad70e06eb805f7d136c3a4db6eb3ea1e2dcf760' href='/packages/Containers-immersionday-workshop/commits/7ad70e06eb805f7d136c3a4db6eb3ea1e2dcf760'>7ad70e06</a>
</div>
</div>


</div>
<p class='top-buffer'>
<span class='subject'>
<a href="/packages/Containers-immersionday-workshop/commits/c561dea942838bc0e25029134936a482af94a5da">first commit</a>
</span>
</p>
</div>
<div id='related_items'>
<h3>Related Items</h3>
<div class='fetching subtext'>
Fetching...
</div>
<div class='msg subtext' style='display: none'>
No related items found.
</div>
<ul data-bind='foreach: relatedItemsModel().relatedItems, visible: relatedItemsModel().relatedItems().length &gt; 0'>
<li>
<span data-bind='text: type'></span>
<a data-bind='text: link.title, attr: {href: link.url}'></a>
<a class='delete_relation' data-bind="attr: {href: '/delete-relation?eid=' + link.eid}" onclick='return confirm("Really delete this relation?")'>
<span class='red'>&nbsp;x&nbsp;</span>
</a>
</li>
</ul>
<div class='add_relation_link'>
<a href='#'>+ Add Relation</a>
</div>
<div class='add_related_items'>
<form action="/create_relation" accept-charset="UTF-8" method="post"><input name="utf8" type="hidden" value="&#x2713;" /><input type="hidden" name="authenticity_token" value="RdxSfoBztoeaC96Yak4Cxc4I2ahdYZhSASdiExn1liwQDqILsuHSHApV0xbqVAbHJy6RLbp44Cigsr/C1EMhXw==" />
Relate this commit to url:
<input name='relation' type='text'>
<input type="hidden" name="package_id" id="package_id" value="Containers-immersionday-workshop" />
<input type="hidden" name="commit_id" id="commit_id" value="c561dea942838bc0e25029134936a482af94a5da" />
<input type="submit" name="commit" value="Save" class="btn btn-default" />
</form>

</div>
</div>
</div>
</div>

</div>
</div>
</div>
<div class='clear'></div>

<div class='jump_to_file hidden-print'>
<div class='jump_to_file_form'>
<form class='form_inline' onSubmit='return false'>
<input type="hidden" name="package_id" id="package_id" value="Containers-immersionday-workshop" />
<input type="hidden" name="commit_id_for_file" id="commit_id_for_file" value="mainline" />
<div class='input-append'>
<input accesskey='j' class='hinted form-control search' id='filesearch' name='file' placeholder='Jump to a file' title='Jump to a file' type='text'>
</div>
<div class='jump_to_file_dismiss'></div>
</form>
</div>
<div class='jump_to_file_popup'><a class='help helpPopup' data-content="Here you can enter the name of the file and it will provide suggestions with the matching file names and the path for the same.&lt;br/&gt; After selecting the required file, it will redirect to that file. The keyboard shortcut is 'CTRL+j'.">
<img src='https://internal-cdn.amazon.com/btk.amazon.com/img/icons-1.0/tooltip-bubble.png'>
</a>
</div>
<div class='jump_to_file_error'>
The above file can not be found. Either the whole path is missing or the file is not in
<br>this package. Please check the autosuggestions.</br>
</div>
</div>

<!--
mime_type: text/plain; charset=utf-8
-->
<div class='file_header'>
<div class='path_breadcrumbs'>
<div class='path_breadcrumbs'>
<span class='path_breadcrumb'><a href="/packages/Containers-immersionday-workshop">Containers-immersionday-workshop</a></span>/<span class='path_breadcrumb'><a href="/packages/Containers-immersionday-workshop/trees/mainline/--/">mainline</a></span>/<span class='path_breadcrumb'>README.md</span>
</div>

</div>
<div class='hidden-print' id='file_actions'>
<ul class='button_group'>
<li>
<a class="minibutton" href="/packages/Containers-immersionday-workshop/blobs/mainline/--/README.md?raw=1">Raw</a>
</li>
<li>
<a class="minibutton" href="/packages/Containers-immersionday-workshop/blobs/mainline/--/README.md?download=1">Download</a>
</li>
<li>
<a class="minibutton" href="/packages/Containers-immersionday-workshop/logs/mainline?path=README.md">History</a>
</li>
<li>
<a class="minibutton" href="/packages/Containers-immersionday-workshop/blobs/mainline/--/README.md/edit_file_online">Edit</a>
</li>
<li>
<a class="minibutton md_control_raw" href="#raw_markdown">Markdown Source</a>
</li>
<li>
<a class="minibutton md_control_rendered selected active" href="#">Rendered Markdown</a>
</li>
<li class='permalink'>
<a class="minibutton" href="/packages/Containers-immersionday-workshop/blobs/c561dea942838bc0e25029134936a482af94a5da/--/README.md">Permalink</a>
</li>
</ul>
</div>
<div class='clear'></div>
<markdown add-raw-if-needed='true'>
# Provision Accounts for Container Day labs using Event Engine



## Event Engine

The AWS Event Engine was created to help AWS field teams run Workshops, GameDays, Bootcamps, Immersion Days,
and other events that require hands-on access to AWS accounts.

For introduction and please refer to [onboarding guide](https://w.amazon.com/bin/view/AWS_EventEngine/)

## Create Event engine module and blueprint

### Introduction

A module is a self-contained piece of content that can be consumed by customers. For example, EKS Lab in a
[workshop](http://labs.awscontainerday.com/eks.html). A module can be comprised of a master template, a team
template, a readme, an IAM policy, and any additional artifacts. Once you've defined your module, you can then build a
Blueprint by selecting this, and possibly other modules, together.

In the following section we will look at how you can build a module using existing [template](EE_team_template.yaml). We will then create a blue print to provision accounts using these modules.

&gt; Please make sure to review the template before you proceed. For example, EKS template has the eksctl configuration file embedded in CFN. It uses us-east-1 as default region and Kubernetes v1.16 as default version. You can also add any other configuration supported by eksctl.

### Create a module 

1. Browse to [event engine](https://admin.eventengine.run) and click on Backend -&gt; Module

| **EE Home Page** |
|:--:| 
| ![EE Home Page](images/ee_create_module_or_blueprint.png) | 

***

| **Create Module** |
|:--:| 
| ![Create module](images/ee_create_module.png) | 




2. Specify name, label and description for your module and click create.

| **Module Details** |
|:--:| 
| ![Module Details](images/module_details.png) | 


3. Once a module is created, proceed to customizing your module by using cloudformation template and custom IAM policies.

| **Edit Config** |
|:--:| 
| ![Edit Config](images/ee_config_module.png) | 

4. Start with defining an IAM settings for the users. Use [IAM Policy Statements](EE_IAM.json) and [IAM Trusted Services](EE_IAM_trust_policy.txt)

| **Module IAM Config** |
|:--:| 
| ![Module IAM Config](images/ee_module_iam_config.png) | 

5. Next, update team template. This is used to provision resources used for Lab and click save.

| **Module Team template** |
|:--:| 
| ![Module team template](images/ee_module_team_template.png) | 

&gt; This template will provision - 
&gt; Cloud9 IDE for ECS Labs and EKS Cluster usiing m5.xlarge worker nodes. 
&gt; Cloud9 IDE for ECS Labs and a Fargate Cluster.

| **Save module** |
|:--:| 
| ![Save module](images/save_module.png) | 

### Create a blueprint 


1. Browse to [event engine](https://admin.eventengine.run) and click on Backend -&gt; Blueprint -&gt; Create Blueprint

| **EE Home Page** |
|:--:| 
| ![EE Home Page](images/ee_create_module_or_blueprint.png) | 


2. Provide blueprint Type, Name, description and click Create

| **Create blueprint** |
|:--:| 
| ![Create Blueprint](images/create_blueprint.png) | 


3. Add module(s) to your blueprint and Click save.

| **Add module to blueprint 1/3** |
|:--:| 
| ![Save module](images/add_module_to_blueprint.png) | 

***

| **Add module to blueprint 2/3** |
|:--:| 
| ![Save module](images/add_module_template.png) | 

***

| **Add module to blueprint 3/3** |
|:--:| 
| ![Save module](images/save_blueprint.png) | 

## Provision Accounts 

1. Browse to [event engine](https://admin.eventengine.run) and click on Create Event

2. Select blueprint

| **Add module to blueprint 3/3** |
|:--:| 
| ![Save module](images/create_event_1.png) | 


3. Provide Event Details

| **Add module to blueprint 3/3** |
|:--:| 
| ![Save module](images/create_event_2.png) | 


4. Team and Customer Information

| **Add module to blueprint 3/3** |
|:--:| 
| ![Save module](images/create_event_3.png) | 


5. Initialize and Monitor Event

&gt;It will take a while before accounts are provisioned. Meanwhile you can export account hash and keep them ready to
&gt; be printed or emailed. Check back after a while to make sure all accounts are successfully provisioned.

| **Add module to blueprint 3/3** |
|:--:| 
| ![Save module](images/create_event_4.png) | 

&gt; All status squares should be green. Yellow means provisioning is still in progress, whereas red indicates that account
&gt; wasn’t successfully provisioned.



### Handle transient failures

If an account status is red, you can disable (undeploy) and enable (deploy) module again. This usually helps with any
transient issues during account creation.

| **Manage Account** |
|:--:| 
| ![Troubleshooting Account 1/3](images/manage_account_1.png) | 

***

| **Undeploy module** |
|:--:| 
| ![Troubleshooting Account 2/3](images/manage_account_2.png) | 

***

| **Deploy module** |
|:--:| 
| ![Troubleshooting Account 3/3](images/manage_account_3.png) | 

***


### Export account details

| **Export accounts details** |
|:--:| 
| ![Export accounts details](images/export_account.png) | 

***

### Terminate Event

&gt; Always remember to terminate event on completion.

| **Terminate Event** |
|:--:| 
| ![Terminate Event](images/terminate_event.png) | 
</markdown>
<div class='blob hidden-print highlighttable markdown_source' ng_non_bindable>
    <div class="js-syntax-highlight-wrapper">
      <table class="code js-syntax-highlight">
        <tbody>
            <tr class="line_holder" id="L1">
              <td class="line-num" data-linenumber="1">
                <span class="linked-line" unselectable="on" data-linenumber="1"></span>
              </td>
              <td class="line_content"><span class="gh"># Provision Accounts for Container Day labs using Event Engine</span>
</td>
            </tr>
            <tr class="line_holder" id="L2">
              <td class="line-num" data-linenumber="2">
                <span class="linked-line" unselectable="on" data-linenumber="2"></span>
              </td>
              <td class="line_content">
</td>
            </tr>
            <tr class="line_holder" id="L3">
              <td class="line-num" data-linenumber="3">
                <span class="linked-line" unselectable="on" data-linenumber="3"></span>
              </td>
              <td class="line_content">
</td>
            </tr>
            <tr class="line_holder" id="L4">
              <td class="line-num" data-linenumber="4">
                <span class="linked-line" unselectable="on" data-linenumber="4"></span>
              </td>
              <td class="line_content">
</td>
            </tr>
            <tr class="line_holder" id="L5">
              <td class="line-num" data-linenumber="5">
                <span class="linked-line" unselectable="on" data-linenumber="5"></span>
              </td>
              <td class="line_content"><span class="gu">## Event Engine</span>
</td>
            </tr>
            <tr class="line_holder" id="L6">
              <td class="line-num" data-linenumber="6">
                <span class="linked-line" unselectable="on" data-linenumber="6"></span>
              </td>
              <td class="line_content">
</td>
            </tr>
            <tr class="line_holder" id="L7">
              <td class="line-num" data-linenumber="7">
                <span class="linked-line" unselectable="on" data-linenumber="7"></span>
              </td>
              <td class="line_content">The AWS Event Engine was created to help AWS field teams run Workshops, GameDays, Bootcamps, Immersion Days,
</td>
            </tr>
            <tr class="line_holder" id="L8">
              <td class="line-num" data-linenumber="8">
                <span class="linked-line" unselectable="on" data-linenumber="8"></span>
              </td>
              <td class="line_content">and other events that require hands-on access to AWS accounts.
</td>
            </tr>
            <tr class="line_holder" id="L9">
              <td class="line-num" data-linenumber="9">
                <span class="linked-line" unselectable="on" data-linenumber="9"></span>
              </td>
              <td class="line_content">
</td>
            </tr>
            <tr class="line_holder" id="L10">
              <td class="line-num" data-linenumber="10">
                <span class="linked-line" unselectable="on" data-linenumber="10"></span>
              </td>
              <td class="line_content">For introduction and please refer to <span class="p">[</span><span class="nv">onboarding guide</span><span class="p">](</span><span class="sx">https://w.amazon.com/bin/view/AWS_EventEngine/</span><span class="p">)</span>
</td>
            </tr>
            <tr class="line_holder" id="L11">
              <td class="line-num" data-linenumber="11">
                <span class="linked-line" unselectable="on" data-linenumber="11"></span>
              </td>
              <td class="line_content">
</td>
            </tr>
            <tr class="line_holder" id="L12">
              <td class="line-num" data-linenumber="12">
                <span class="linked-line" unselectable="on" data-linenumber="12"></span>
              </td>
              <td class="line_content"><span class="gu">## Create Event engine module and blueprint</span>
</td>
            </tr>
            <tr class="line_holder" id="L13">
              <td class="line-num" data-linenumber="13">
                <span class="linked-line" unselectable="on" data-linenumber="13"></span>
              </td>
              <td class="line_content">
</td>
            </tr>
            <tr class="line_holder" id="L14">
              <td class="line-num" data-linenumber="14">
                <span class="linked-line" unselectable="on" data-linenumber="14"></span>
              </td>
              <td class="line_content"><span class="gu">### Introduction</span>
</td>
            </tr>
            <tr class="line_holder" id="L15">
              <td class="line-num" data-linenumber="15">
                <span class="linked-line" unselectable="on" data-linenumber="15"></span>
              </td>
              <td class="line_content">
</td>
            </tr>
            <tr class="line_holder" id="L16">
              <td class="line-num" data-linenumber="16">
                <span class="linked-line" unselectable="on" data-linenumber="16"></span>
              </td>
              <td class="line_content">A module is a self-contained piece of content that can be consumed by customers. For example, EKS Lab in a
</td>
            </tr>
            <tr class="line_holder" id="L17">
              <td class="line-num" data-linenumber="17">
                <span class="linked-line" unselectable="on" data-linenumber="17"></span>
              </td>
              <td class="line_content"><span class="p">[</span><span class="nv">workshop</span><span class="p">](</span><span class="sx">http://labs.awscontainerday.com/eks.html</span><span class="p">)</span>. A module can be comprised of a master template, a team
</td>
            </tr>
            <tr class="line_holder" id="L18">
              <td class="line-num" data-linenumber="18">
                <span class="linked-line" unselectable="on" data-linenumber="18"></span>
              </td>
              <td class="line_content">template, a readme, an IAM policy, and any additional artifacts. Once you've defined your module, you can then build a
</td>
            </tr>
            <tr class="line_holder" id="L19">
              <td class="line-num" data-linenumber="19">
                <span class="linked-line" unselectable="on" data-linenumber="19"></span>
              </td>
              <td class="line_content">Blueprint by selecting this, and possibly other modules, together.
</td>
            </tr>
            <tr class="line_holder" id="L20">
              <td class="line-num" data-linenumber="20">
                <span class="linked-line" unselectable="on" data-linenumber="20"></span>
              </td>
              <td class="line_content">
</td>
            </tr>
            <tr class="line_holder" id="L21">
              <td class="line-num" data-linenumber="21">
                <span class="linked-line" unselectable="on" data-linenumber="21"></span>
              </td>
              <td class="line_content">In the following section we will look at how you can build a module using existing <span class="p">[</span><span class="nv">template</span><span class="p">](</span><span class="sx">EE_team_template.yaml</span><span class="p">)</span>. We will then create a blue print to provision accounts using these modules.
</td>
            </tr>
            <tr class="line_holder" id="L22">
              <td class="line-num" data-linenumber="22">
                <span class="linked-line" unselectable="on" data-linenumber="22"></span>
              </td>
              <td class="line_content">
</td>
            </tr>
            <tr class="line_holder" id="L23">
              <td class="line-num" data-linenumber="23">
                <span class="linked-line" unselectable="on" data-linenumber="23"></span>
              </td>
              <td class="line_content"><span class="gt">&gt; Please make sure to review the template before you proceed. For example, EKS template has the eksctl configuration file embedded in CFN. It uses us-east-1 as default region and Kubernetes v1.16 as default version. You can also add any other configuration supported by eksctl.</span>
</td>
            </tr>
            <tr class="line_holder" id="L24">
              <td class="line-num" data-linenumber="24">
                <span class="linked-line" unselectable="on" data-linenumber="24"></span>
              </td>
              <td class="line_content">
</td>
            </tr>
            <tr class="line_holder" id="L25">
              <td class="line-num" data-linenumber="25">
                <span class="linked-line" unselectable="on" data-linenumber="25"></span>
              </td>
              <td class="line_content"><span class="gu">### Create a module </span>
</td>
            </tr>
            <tr class="line_holder" id="L26">
              <td class="line-num" data-linenumber="26">
                <span class="linked-line" unselectable="on" data-linenumber="26"></span>
              </td>
              <td class="line_content">
</td>
            </tr>
            <tr class="line_holder" id="L27">
              <td class="line-num" data-linenumber="27">
                <span class="linked-line" unselectable="on" data-linenumber="27"></span>
              </td>
              <td class="line_content"><span class="p">1.</span> Browse to <span class="p">[</span><span class="nv">event engine</span><span class="p">](</span><span class="sx">https://admin.eventengine.run</span><span class="p">)</span> and click on Backend -&gt; Module
</td>
            </tr>
            <tr class="line_holder" id="L28">
              <td class="line-num" data-linenumber="28">
                <span class="linked-line" unselectable="on" data-linenumber="28"></span>
              </td>
              <td class="line_content">
</td>
            </tr>
            <tr class="line_holder" id="L29">
              <td class="line-num" data-linenumber="29">
                <span class="linked-line" unselectable="on" data-linenumber="29"></span>
              </td>
              <td class="line_content">| <span class="gs">**EE Home Page**</span> |
</td>
            </tr>
            <tr class="line_holder" id="L30">
              <td class="line-num" data-linenumber="30">
                <span class="linked-line" unselectable="on" data-linenumber="30"></span>
              </td>
              <td class="line_content">|:--:| 
</td>
            </tr>
            <tr class="line_holder" id="L31">
              <td class="line-num" data-linenumber="31">
                <span class="linked-line" unselectable="on" data-linenumber="31"></span>
              </td>
              <td class="line_content">| !<span class="p">[</span><span class="nv">EE Home Page</span><span class="p">](</span><span class="sx">images/ee_create_module_or_blueprint.png</span><span class="p">)</span> | 
</td>
            </tr>
            <tr class="line_holder" id="L32">
              <td class="line-num" data-linenumber="32">
                <span class="linked-line" unselectable="on" data-linenumber="32"></span>
              </td>
              <td class="line_content">
</td>
            </tr>
            <tr class="line_holder" id="L33">
              <td class="line-num" data-linenumber="33">
                <span class="linked-line" unselectable="on" data-linenumber="33"></span>
              </td>
              <td class="line_content"><span class="p">***</span>
</td>
            </tr>
            <tr class="line_holder" id="L34">
              <td class="line-num" data-linenumber="34">
                <span class="linked-line" unselectable="on" data-linenumber="34"></span>
              </td>
              <td class="line_content">
</td>
            </tr>
            <tr class="line_holder" id="L35">
              <td class="line-num" data-linenumber="35">
                <span class="linked-line" unselectable="on" data-linenumber="35"></span>
              </td>
              <td class="line_content">| <span class="gs">**Create Module**</span> |
</td>
            </tr>
            <tr class="line_holder" id="L36">
              <td class="line-num" data-linenumber="36">
                <span class="linked-line" unselectable="on" data-linenumber="36"></span>
              </td>
              <td class="line_content">|:--:| 
</td>
            </tr>
            <tr class="line_holder" id="L37">
              <td class="line-num" data-linenumber="37">
                <span class="linked-line" unselectable="on" data-linenumber="37"></span>
              </td>
              <td class="line_content">| !<span class="p">[</span><span class="nv">Create module</span><span class="p">](</span><span class="sx">images/ee_create_module.png</span><span class="p">)</span> | 
</td>
            </tr>
            <tr class="line_holder" id="L38">
              <td class="line-num" data-linenumber="38">
                <span class="linked-line" unselectable="on" data-linenumber="38"></span>
              </td>
              <td class="line_content">
</td>
            </tr>
            <tr class="line_holder" id="L39">
              <td class="line-num" data-linenumber="39">
                <span class="linked-line" unselectable="on" data-linenumber="39"></span>
              </td>
              <td class="line_content">
</td>
            </tr>
            <tr class="line_holder" id="L40">
              <td class="line-num" data-linenumber="40">
                <span class="linked-line" unselectable="on" data-linenumber="40"></span>
              </td>
              <td class="line_content">
</td>
            </tr>
            <tr class="line_holder" id="L41">
              <td class="line-num" data-linenumber="41">
                <span class="linked-line" unselectable="on" data-linenumber="41"></span>
              </td>
              <td class="line_content">
</td>
            </tr>
            <tr class="line_holder" id="L42">
              <td class="line-num" data-linenumber="42">
                <span class="linked-line" unselectable="on" data-linenumber="42"></span>
              </td>
              <td class="line_content"><span class="p">2.</span> Specify name, label and description for your module and click create.
</td>
            </tr>
            <tr class="line_holder" id="L43">
              <td class="line-num" data-linenumber="43">
                <span class="linked-line" unselectable="on" data-linenumber="43"></span>
              </td>
              <td class="line_content">
</td>
            </tr>
            <tr class="line_holder" id="L44">
              <td class="line-num" data-linenumber="44">
                <span class="linked-line" unselectable="on" data-linenumber="44"></span>
              </td>
              <td class="line_content">| <span class="gs">**Module Details**</span> |
</td>
            </tr>
            <tr class="line_holder" id="L45">
              <td class="line-num" data-linenumber="45">
                <span class="linked-line" unselectable="on" data-linenumber="45"></span>
              </td>
              <td class="line_content">|:--:| 
</td>
            </tr>
            <tr class="line_holder" id="L46">
              <td class="line-num" data-linenumber="46">
                <span class="linked-line" unselectable="on" data-linenumber="46"></span>
              </td>
              <td class="line_content">| !<span class="p">[</span><span class="nv">Module Details</span><span class="p">](</span><span class="sx">images/module_details.png</span><span class="p">)</span> | 
</td>
            </tr>
            <tr class="line_holder" id="L47">
              <td class="line-num" data-linenumber="47">
                <span class="linked-line" unselectable="on" data-linenumber="47"></span>
              </td>
              <td class="line_content">
</td>
            </tr>
            <tr class="line_holder" id="L48">
              <td class="line-num" data-linenumber="48">
                <span class="linked-line" unselectable="on" data-linenumber="48"></span>
              </td>
              <td class="line_content">
</td>
            </tr>
            <tr class="line_holder" id="L49">
              <td class="line-num" data-linenumber="49">
                <span class="linked-line" unselectable="on" data-linenumber="49"></span>
              </td>
              <td class="line_content"><span class="p">3.</span> Once a module is created, proceed to customizing your module by using cloudformation template and custom IAM policies.
</td>
            </tr>
            <tr class="line_holder" id="L50">
              <td class="line-num" data-linenumber="50">
                <span class="linked-line" unselectable="on" data-linenumber="50"></span>
              </td>
              <td class="line_content">
</td>
            </tr>
            <tr class="line_holder" id="L51">
              <td class="line-num" data-linenumber="51">
                <span class="linked-line" unselectable="on" data-linenumber="51"></span>
              </td>
              <td class="line_content">| <span class="gs">**Edit Config**</span> |
</td>
            </tr>
            <tr class="line_holder" id="L52">
              <td class="line-num" data-linenumber="52">
                <span class="linked-line" unselectable="on" data-linenumber="52"></span>
              </td>
              <td class="line_content">|:--:| 
</td>
            </tr>
            <tr class="line_holder" id="L53">
              <td class="line-num" data-linenumber="53">
                <span class="linked-line" unselectable="on" data-linenumber="53"></span>
              </td>
              <td class="line_content">| !<span class="p">[</span><span class="nv">Edit Config</span><span class="p">](</span><span class="sx">images/ee_config_module.png</span><span class="p">)</span> | 
</td>
            </tr>
            <tr class="line_holder" id="L54">
              <td class="line-num" data-linenumber="54">
                <span class="linked-line" unselectable="on" data-linenumber="54"></span>
              </td>
              <td class="line_content">
</td>
            </tr>
            <tr class="line_holder" id="L55">
              <td class="line-num" data-linenumber="55">
                <span class="linked-line" unselectable="on" data-linenumber="55"></span>
              </td>
              <td class="line_content"><span class="p">4.</span> Start with defining an IAM settings for the users. Use <span class="p">[</span><span class="nv">IAM Policy Statements</span><span class="p">](</span><span class="sx">EE_IAM.json</span><span class="p">)</span> and <span class="p">[</span><span class="nv">IAM Trusted Services</span><span class="p">](</span><span class="sx">EE_IAM_trust_policy.txt</span><span class="p">)</span>
</td>
            </tr>
            <tr class="line_holder" id="L56">
              <td class="line-num" data-linenumber="56">
                <span class="linked-line" unselectable="on" data-linenumber="56"></span>
              </td>
              <td class="line_content">
</td>
            </tr>
            <tr class="line_holder" id="L57">
              <td class="line-num" data-linenumber="57">
                <span class="linked-line" unselectable="on" data-linenumber="57"></span>
              </td>
              <td class="line_content">| <span class="gs">**Module IAM Config**</span> |
</td>
            </tr>
            <tr class="line_holder" id="L58">
              <td class="line-num" data-linenumber="58">
                <span class="linked-line" unselectable="on" data-linenumber="58"></span>
              </td>
              <td class="line_content">|:--:| 
</td>
            </tr>
            <tr class="line_holder" id="L59">
              <td class="line-num" data-linenumber="59">
                <span class="linked-line" unselectable="on" data-linenumber="59"></span>
              </td>
              <td class="line_content">| !<span class="p">[</span><span class="nv">Module IAM Config</span><span class="p">](</span><span class="sx">images/ee_module_iam_config.png</span><span class="p">)</span> | 
</td>
            </tr>
            <tr class="line_holder" id="L60">
              <td class="line-num" data-linenumber="60">
                <span class="linked-line" unselectable="on" data-linenumber="60"></span>
              </td>
              <td class="line_content">
</td>
            </tr>
            <tr class="line_holder" id="L61">
              <td class="line-num" data-linenumber="61">
                <span class="linked-line" unselectable="on" data-linenumber="61"></span>
              </td>
              <td class="line_content"><span class="p">5.</span> Next, update team template. This is used to provision resources used for Lab and click save.
</td>
            </tr>
            <tr class="line_holder" id="L62">
              <td class="line-num" data-linenumber="62">
                <span class="linked-line" unselectable="on" data-linenumber="62"></span>
              </td>
              <td class="line_content">
</td>
            </tr>
            <tr class="line_holder" id="L63">
              <td class="line-num" data-linenumber="63">
                <span class="linked-line" unselectable="on" data-linenumber="63"></span>
              </td>
              <td class="line_content">| <span class="gs">**Module Team template**</span> |
</td>
            </tr>
            <tr class="line_holder" id="L64">
              <td class="line-num" data-linenumber="64">
                <span class="linked-line" unselectable="on" data-linenumber="64"></span>
              </td>
              <td class="line_content">|:--:| 
</td>
            </tr>
            <tr class="line_holder" id="L65">
              <td class="line-num" data-linenumber="65">
                <span class="linked-line" unselectable="on" data-linenumber="65"></span>
              </td>
              <td class="line_content">| !<span class="p">[</span><span class="nv">Module team template</span><span class="p">](</span><span class="sx">images/ee_module_team_template.png</span><span class="p">)</span> | 
</td>
            </tr>
            <tr class="line_holder" id="L66">
              <td class="line-num" data-linenumber="66">
                <span class="linked-line" unselectable="on" data-linenumber="66"></span>
              </td>
              <td class="line_content">
</td>
            </tr>
            <tr class="line_holder" id="L67">
              <td class="line-num" data-linenumber="67">
                <span class="linked-line" unselectable="on" data-linenumber="67"></span>
              </td>
              <td class="line_content"><span class="gt">&gt; This template will provision - </span>
</td>
            </tr>
            <tr class="line_holder" id="L68">
              <td class="line-num" data-linenumber="68">
                <span class="linked-line" unselectable="on" data-linenumber="68"></span>
              </td>
              <td class="line_content"><span class="gt">&gt; Cloud9 IDE for ECS Labs and EKS Cluster usiing m5.xlarge worker nodes. </span>
</td>
            </tr>
            <tr class="line_holder" id="L69">
              <td class="line-num" data-linenumber="69">
                <span class="linked-line" unselectable="on" data-linenumber="69"></span>
              </td>
              <td class="line_content"><span class="gt">&gt; Cloud9 IDE for ECS Labs and a Fargate Cluster.</span>
</td>
            </tr>
            <tr class="line_holder" id="L70">
              <td class="line-num" data-linenumber="70">
                <span class="linked-line" unselectable="on" data-linenumber="70"></span>
              </td>
              <td class="line_content">
</td>
            </tr>
            <tr class="line_holder" id="L71">
              <td class="line-num" data-linenumber="71">
                <span class="linked-line" unselectable="on" data-linenumber="71"></span>
              </td>
              <td class="line_content">| <span class="gs">**Save module**</span> |
</td>
            </tr>
            <tr class="line_holder" id="L72">
              <td class="line-num" data-linenumber="72">
                <span class="linked-line" unselectable="on" data-linenumber="72"></span>
              </td>
              <td class="line_content">|:--:| 
</td>
            </tr>
            <tr class="line_holder" id="L73">
              <td class="line-num" data-linenumber="73">
                <span class="linked-line" unselectable="on" data-linenumber="73"></span>
              </td>
              <td class="line_content">| !<span class="p">[</span><span class="nv">Save module</span><span class="p">](</span><span class="sx">images/save_module.png</span><span class="p">)</span> | 
</td>
            </tr>
            <tr class="line_holder" id="L74">
              <td class="line-num" data-linenumber="74">
                <span class="linked-line" unselectable="on" data-linenumber="74"></span>
              </td>
              <td class="line_content">
</td>
            </tr>
            <tr class="line_holder" id="L75">
              <td class="line-num" data-linenumber="75">
                <span class="linked-line" unselectable="on" data-linenumber="75"></span>
              </td>
              <td class="line_content"><span class="gu">### Create a blueprint </span>
</td>
            </tr>
            <tr class="line_holder" id="L76">
              <td class="line-num" data-linenumber="76">
                <span class="linked-line" unselectable="on" data-linenumber="76"></span>
              </td>
              <td class="line_content">
</td>
            </tr>
            <tr class="line_holder" id="L77">
              <td class="line-num" data-linenumber="77">
                <span class="linked-line" unselectable="on" data-linenumber="77"></span>
              </td>
              <td class="line_content">
</td>
            </tr>
            <tr class="line_holder" id="L78">
              <td class="line-num" data-linenumber="78">
                <span class="linked-line" unselectable="on" data-linenumber="78"></span>
              </td>
              <td class="line_content"><span class="p">1.</span> Browse to <span class="p">[</span><span class="nv">event engine</span><span class="p">](</span><span class="sx">https://admin.eventengine.run</span><span class="p">)</span> and click on Backend -&gt; Blueprint -&gt; Create Blueprint
</td>
            </tr>
            <tr class="line_holder" id="L79">
              <td class="line-num" data-linenumber="79">
                <span class="linked-line" unselectable="on" data-linenumber="79"></span>
              </td>
              <td class="line_content">
</td>
            </tr>
            <tr class="line_holder" id="L80">
              <td class="line-num" data-linenumber="80">
                <span class="linked-line" unselectable="on" data-linenumber="80"></span>
              </td>
              <td class="line_content">| <span class="gs">**EE Home Page**</span> |
</td>
            </tr>
            <tr class="line_holder" id="L81">
              <td class="line-num" data-linenumber="81">
                <span class="linked-line" unselectable="on" data-linenumber="81"></span>
              </td>
              <td class="line_content">|:--:| 
</td>
            </tr>
            <tr class="line_holder" id="L82">
              <td class="line-num" data-linenumber="82">
                <span class="linked-line" unselectable="on" data-linenumber="82"></span>
              </td>
              <td class="line_content">| !<span class="p">[</span><span class="nv">EE Home Page</span><span class="p">](</span><span class="sx">images/ee_create_module_or_blueprint.png</span><span class="p">)</span> | 
</td>
            </tr>
            <tr class="line_holder" id="L83">
              <td class="line-num" data-linenumber="83">
                <span class="linked-line" unselectable="on" data-linenumber="83"></span>
              </td>
              <td class="line_content">
</td>
            </tr>
            <tr class="line_holder" id="L84">
              <td class="line-num" data-linenumber="84">
                <span class="linked-line" unselectable="on" data-linenumber="84"></span>
              </td>
              <td class="line_content">
</td>
            </tr>
            <tr class="line_holder" id="L85">
              <td class="line-num" data-linenumber="85">
                <span class="linked-line" unselectable="on" data-linenumber="85"></span>
              </td>
              <td class="line_content"><span class="p">2.</span> Provide blueprint Type, Name, description and click Create
</td>
            </tr>
            <tr class="line_holder" id="L86">
              <td class="line-num" data-linenumber="86">
                <span class="linked-line" unselectable="on" data-linenumber="86"></span>
              </td>
              <td class="line_content">
</td>
            </tr>
            <tr class="line_holder" id="L87">
              <td class="line-num" data-linenumber="87">
                <span class="linked-line" unselectable="on" data-linenumber="87"></span>
              </td>
              <td class="line_content">| <span class="gs">**Create blueprint**</span> |
</td>
            </tr>
            <tr class="line_holder" id="L88">
              <td class="line-num" data-linenumber="88">
                <span class="linked-line" unselectable="on" data-linenumber="88"></span>
              </td>
              <td class="line_content">|:--:| 
</td>
            </tr>
            <tr class="line_holder" id="L89">
              <td class="line-num" data-linenumber="89">
                <span class="linked-line" unselectable="on" data-linenumber="89"></span>
              </td>
              <td class="line_content">| !<span class="p">[</span><span class="nv">Create Blueprint</span><span class="p">](</span><span class="sx">images/create_blueprint.png</span><span class="p">)</span> | 
</td>
            </tr>
            <tr class="line_holder" id="L90">
              <td class="line-num" data-linenumber="90">
                <span class="linked-line" unselectable="on" data-linenumber="90"></span>
              </td>
              <td class="line_content">
</td>
            </tr>
            <tr class="line_holder" id="L91">
              <td class="line-num" data-linenumber="91">
                <span class="linked-line" unselectable="on" data-linenumber="91"></span>
              </td>
              <td class="line_content">
</td>
            </tr>
            <tr class="line_holder" id="L92">
              <td class="line-num" data-linenumber="92">
                <span class="linked-line" unselectable="on" data-linenumber="92"></span>
              </td>
              <td class="line_content"><span class="p">3.</span> Add module(s) to your blueprint and Click save.
</td>
            </tr>
            <tr class="line_holder" id="L93">
              <td class="line-num" data-linenumber="93">
                <span class="linked-line" unselectable="on" data-linenumber="93"></span>
              </td>
              <td class="line_content">
</td>
            </tr>
            <tr class="line_holder" id="L94">
              <td class="line-num" data-linenumber="94">
                <span class="linked-line" unselectable="on" data-linenumber="94"></span>
              </td>
              <td class="line_content">| <span class="gs">**Add module to blueprint 1/3**</span> |
</td>
            </tr>
            <tr class="line_holder" id="L95">
              <td class="line-num" data-linenumber="95">
                <span class="linked-line" unselectable="on" data-linenumber="95"></span>
              </td>
              <td class="line_content">|:--:| 
</td>
            </tr>
            <tr class="line_holder" id="L96">
              <td class="line-num" data-linenumber="96">
                <span class="linked-line" unselectable="on" data-linenumber="96"></span>
              </td>
              <td class="line_content">| !<span class="p">[</span><span class="nv">Save module</span><span class="p">](</span><span class="sx">images/add_module_to_blueprint.png</span><span class="p">)</span> | 
</td>
            </tr>
            <tr class="line_holder" id="L97">
              <td class="line-num" data-linenumber="97">
                <span class="linked-line" unselectable="on" data-linenumber="97"></span>
              </td>
              <td class="line_content">
</td>
            </tr>
            <tr class="line_holder" id="L98">
              <td class="line-num" data-linenumber="98">
                <span class="linked-line" unselectable="on" data-linenumber="98"></span>
              </td>
              <td class="line_content"><span class="p">***</span>
</td>
            </tr>
            <tr class="line_holder" id="L99">
              <td class="line-num" data-linenumber="99">
                <span class="linked-line" unselectable="on" data-linenumber="99"></span>
              </td>
              <td class="line_content">
</td>
            </tr>
            <tr class="line_holder" id="L100">
              <td class="line-num" data-linenumber="100">
                <span class="linked-line" unselectable="on" data-linenumber="100"></span>
              </td>
              <td class="line_content">| <span class="gs">**Add module to blueprint 2/3**</span> |
</td>
            </tr>
            <tr class="line_holder" id="L101">
              <td class="line-num" data-linenumber="101">
                <span class="linked-line" unselectable="on" data-linenumber="101"></span>
              </td>
              <td class="line_content">|:--:| 
</td>
            </tr>
            <tr class="line_holder" id="L102">
              <td class="line-num" data-linenumber="102">
                <span class="linked-line" unselectable="on" data-linenumber="102"></span>
              </td>
              <td class="line_content">| !<span class="p">[</span><span class="nv">Save module</span><span class="p">](</span><span class="sx">images/add_module_template.png</span><span class="p">)</span> | 
</td>
            </tr>
            <tr class="line_holder" id="L103">
              <td class="line-num" data-linenumber="103">
                <span class="linked-line" unselectable="on" data-linenumber="103"></span>
              </td>
              <td class="line_content">
</td>
            </tr>
            <tr class="line_holder" id="L104">
              <td class="line-num" data-linenumber="104">
                <span class="linked-line" unselectable="on" data-linenumber="104"></span>
              </td>
              <td class="line_content"><span class="p">***</span>
</td>
            </tr>
            <tr class="line_holder" id="L105">
              <td class="line-num" data-linenumber="105">
                <span class="linked-line" unselectable="on" data-linenumber="105"></span>
              </td>
              <td class="line_content">
</td>
            </tr>
            <tr class="line_holder" id="L106">
              <td class="line-num" data-linenumber="106">
                <span class="linked-line" unselectable="on" data-linenumber="106"></span>
              </td>
              <td class="line_content">| <span class="gs">**Add module to blueprint 3/3**</span> |
</td>
            </tr>
            <tr class="line_holder" id="L107">
              <td class="line-num" data-linenumber="107">
                <span class="linked-line" unselectable="on" data-linenumber="107"></span>
              </td>
              <td class="line_content">|:--:| 
</td>
            </tr>
            <tr class="line_holder" id="L108">
              <td class="line-num" data-linenumber="108">
                <span class="linked-line" unselectable="on" data-linenumber="108"></span>
              </td>
              <td class="line_content">| !<span class="p">[</span><span class="nv">Save module</span><span class="p">](</span><span class="sx">images/save_blueprint.png</span><span class="p">)</span> | 
</td>
            </tr>
            <tr class="line_holder" id="L109">
              <td class="line-num" data-linenumber="109">
                <span class="linked-line" unselectable="on" data-linenumber="109"></span>
              </td>
              <td class="line_content">
</td>
            </tr>
            <tr class="line_holder" id="L110">
              <td class="line-num" data-linenumber="110">
                <span class="linked-line" unselectable="on" data-linenumber="110"></span>
              </td>
              <td class="line_content"><span class="gu">## Provision Accounts </span>
</td>
            </tr>
            <tr class="line_holder" id="L111">
              <td class="line-num" data-linenumber="111">
                <span class="linked-line" unselectable="on" data-linenumber="111"></span>
              </td>
              <td class="line_content">
</td>
            </tr>
            <tr class="line_holder" id="L112">
              <td class="line-num" data-linenumber="112">
                <span class="linked-line" unselectable="on" data-linenumber="112"></span>
              </td>
              <td class="line_content"><span class="p">1.</span> Browse to <span class="p">[</span><span class="nv">event engine</span><span class="p">](</span><span class="sx">https://admin.eventengine.run</span><span class="p">)</span> and click on Create Event
</td>
            </tr>
            <tr class="line_holder" id="L113">
              <td class="line-num" data-linenumber="113">
                <span class="linked-line" unselectable="on" data-linenumber="113"></span>
              </td>
              <td class="line_content">
</td>
            </tr>
            <tr class="line_holder" id="L114">
              <td class="line-num" data-linenumber="114">
                <span class="linked-line" unselectable="on" data-linenumber="114"></span>
              </td>
              <td class="line_content"><span class="p">2.</span> Select blueprint
</td>
            </tr>
            <tr class="line_holder" id="L115">
              <td class="line-num" data-linenumber="115">
                <span class="linked-line" unselectable="on" data-linenumber="115"></span>
              </td>
              <td class="line_content">
</td>
            </tr>
            <tr class="line_holder" id="L116">
              <td class="line-num" data-linenumber="116">
                <span class="linked-line" unselectable="on" data-linenumber="116"></span>
              </td>
              <td class="line_content">| <span class="gs">**Add module to blueprint 3/3**</span> |
</td>
            </tr>
            <tr class="line_holder" id="L117">
              <td class="line-num" data-linenumber="117">
                <span class="linked-line" unselectable="on" data-linenumber="117"></span>
              </td>
              <td class="line_content">|:--:| 
</td>
            </tr>
            <tr class="line_holder" id="L118">
              <td class="line-num" data-linenumber="118">
                <span class="linked-line" unselectable="on" data-linenumber="118"></span>
              </td>
              <td class="line_content">| !<span class="p">[</span><span class="nv">Save module</span><span class="p">](</span><span class="sx">images/create_event_1.png</span><span class="p">)</span> | 
</td>
            </tr>
            <tr class="line_holder" id="L119">
              <td class="line-num" data-linenumber="119">
                <span class="linked-line" unselectable="on" data-linenumber="119"></span>
              </td>
              <td class="line_content">
</td>
            </tr>
            <tr class="line_holder" id="L120">
              <td class="line-num" data-linenumber="120">
                <span class="linked-line" unselectable="on" data-linenumber="120"></span>
              </td>
              <td class="line_content">
</td>
            </tr>
            <tr class="line_holder" id="L121">
              <td class="line-num" data-linenumber="121">
                <span class="linked-line" unselectable="on" data-linenumber="121"></span>
              </td>
              <td class="line_content"><span class="p">3.</span> Provide Event Details
</td>
            </tr>
            <tr class="line_holder" id="L122">
              <td class="line-num" data-linenumber="122">
                <span class="linked-line" unselectable="on" data-linenumber="122"></span>
              </td>
              <td class="line_content">
</td>
            </tr>
            <tr class="line_holder" id="L123">
              <td class="line-num" data-linenumber="123">
                <span class="linked-line" unselectable="on" data-linenumber="123"></span>
              </td>
              <td class="line_content">| <span class="gs">**Add module to blueprint 3/3**</span> |
</td>
            </tr>
            <tr class="line_holder" id="L124">
              <td class="line-num" data-linenumber="124">
                <span class="linked-line" unselectable="on" data-linenumber="124"></span>
              </td>
              <td class="line_content">|:--:| 
</td>
            </tr>
            <tr class="line_holder" id="L125">
              <td class="line-num" data-linenumber="125">
                <span class="linked-line" unselectable="on" data-linenumber="125"></span>
              </td>
              <td class="line_content">| !<span class="p">[</span><span class="nv">Save module</span><span class="p">](</span><span class="sx">images/create_event_2.png</span><span class="p">)</span> | 
</td>
            </tr>
            <tr class="line_holder" id="L126">
              <td class="line-num" data-linenumber="126">
                <span class="linked-line" unselectable="on" data-linenumber="126"></span>
              </td>
              <td class="line_content">
</td>
            </tr>
            <tr class="line_holder" id="L127">
              <td class="line-num" data-linenumber="127">
                <span class="linked-line" unselectable="on" data-linenumber="127"></span>
              </td>
              <td class="line_content">
</td>
            </tr>
            <tr class="line_holder" id="L128">
              <td class="line-num" data-linenumber="128">
                <span class="linked-line" unselectable="on" data-linenumber="128"></span>
              </td>
              <td class="line_content"><span class="p">4.</span> Team and Customer Information
</td>
            </tr>
            <tr class="line_holder" id="L129">
              <td class="line-num" data-linenumber="129">
                <span class="linked-line" unselectable="on" data-linenumber="129"></span>
              </td>
              <td class="line_content">
</td>
            </tr>
            <tr class="line_holder" id="L130">
              <td class="line-num" data-linenumber="130">
                <span class="linked-line" unselectable="on" data-linenumber="130"></span>
              </td>
              <td class="line_content">| <span class="gs">**Add module to blueprint 3/3**</span> |
</td>
            </tr>
            <tr class="line_holder" id="L131">
              <td class="line-num" data-linenumber="131">
                <span class="linked-line" unselectable="on" data-linenumber="131"></span>
              </td>
              <td class="line_content">|:--:| 
</td>
            </tr>
            <tr class="line_holder" id="L132">
              <td class="line-num" data-linenumber="132">
                <span class="linked-line" unselectable="on" data-linenumber="132"></span>
              </td>
              <td class="line_content">| !<span class="p">[</span><span class="nv">Save module</span><span class="p">](</span><span class="sx">images/create_event_3.png</span><span class="p">)</span> | 
</td>
            </tr>
            <tr class="line_holder" id="L133">
              <td class="line-num" data-linenumber="133">
                <span class="linked-line" unselectable="on" data-linenumber="133"></span>
              </td>
              <td class="line_content">
</td>
            </tr>
            <tr class="line_holder" id="L134">
              <td class="line-num" data-linenumber="134">
                <span class="linked-line" unselectable="on" data-linenumber="134"></span>
              </td>
              <td class="line_content">
</td>
            </tr>
            <tr class="line_holder" id="L135">
              <td class="line-num" data-linenumber="135">
                <span class="linked-line" unselectable="on" data-linenumber="135"></span>
              </td>
              <td class="line_content"><span class="p">5.</span> Initialize and Monitor Event
</td>
            </tr>
            <tr class="line_holder" id="L136">
              <td class="line-num" data-linenumber="136">
                <span class="linked-line" unselectable="on" data-linenumber="136"></span>
              </td>
              <td class="line_content">
</td>
            </tr>
            <tr class="line_holder" id="L137">
              <td class="line-num" data-linenumber="137">
                <span class="linked-line" unselectable="on" data-linenumber="137"></span>
              </td>
              <td class="line_content"><span class="gt">&gt;It will take a while before accounts are provisioned. Meanwhile you can export account hash and keep them ready to</span>
</td>
            </tr>
            <tr class="line_holder" id="L138">
              <td class="line-num" data-linenumber="138">
                <span class="linked-line" unselectable="on" data-linenumber="138"></span>
              </td>
              <td class="line_content"><span class="gt">&gt; be printed or emailed. Check back after a while to make sure all accounts are successfully provisioned.</span>
</td>
            </tr>
            <tr class="line_holder" id="L139">
              <td class="line-num" data-linenumber="139">
                <span class="linked-line" unselectable="on" data-linenumber="139"></span>
              </td>
              <td class="line_content">
</td>
            </tr>
            <tr class="line_holder" id="L140">
              <td class="line-num" data-linenumber="140">
                <span class="linked-line" unselectable="on" data-linenumber="140"></span>
              </td>
              <td class="line_content">| <span class="gs">**Add module to blueprint 3/3**</span> |
</td>
            </tr>
            <tr class="line_holder" id="L141">
              <td class="line-num" data-linenumber="141">
                <span class="linked-line" unselectable="on" data-linenumber="141"></span>
              </td>
              <td class="line_content">|:--:| 
</td>
            </tr>
            <tr class="line_holder" id="L142">
              <td class="line-num" data-linenumber="142">
                <span class="linked-line" unselectable="on" data-linenumber="142"></span>
              </td>
              <td class="line_content">| !<span class="p">[</span><span class="nv">Save module</span><span class="p">](</span><span class="sx">images/create_event_4.png</span><span class="p">)</span> | 
</td>
            </tr>
            <tr class="line_holder" id="L143">
              <td class="line-num" data-linenumber="143">
                <span class="linked-line" unselectable="on" data-linenumber="143"></span>
              </td>
              <td class="line_content">
</td>
            </tr>
            <tr class="line_holder" id="L144">
              <td class="line-num" data-linenumber="144">
                <span class="linked-line" unselectable="on" data-linenumber="144"></span>
              </td>
              <td class="line_content"><span class="gt">&gt; All status squares should be green. Yellow means provisioning is still in progress, whereas red indicates that account</span>
</td>
            </tr>
            <tr class="line_holder" id="L145">
              <td class="line-num" data-linenumber="145">
                <span class="linked-line" unselectable="on" data-linenumber="145"></span>
              </td>
              <td class="line_content"><span class="gt">&gt; wasn’t successfully provisioned.</span>
</td>
            </tr>
            <tr class="line_holder" id="L146">
              <td class="line-num" data-linenumber="146">
                <span class="linked-line" unselectable="on" data-linenumber="146"></span>
              </td>
              <td class="line_content">
</td>
            </tr>
            <tr class="line_holder" id="L147">
              <td class="line-num" data-linenumber="147">
                <span class="linked-line" unselectable="on" data-linenumber="147"></span>
              </td>
              <td class="line_content">
</td>
            </tr>
            <tr class="line_holder" id="L148">
              <td class="line-num" data-linenumber="148">
                <span class="linked-line" unselectable="on" data-linenumber="148"></span>
              </td>
              <td class="line_content">
</td>
            </tr>
            <tr class="line_holder" id="L149">
              <td class="line-num" data-linenumber="149">
                <span class="linked-line" unselectable="on" data-linenumber="149"></span>
              </td>
              <td class="line_content"><span class="gu">### Handle transient failures</span>
</td>
            </tr>
            <tr class="line_holder" id="L150">
              <td class="line-num" data-linenumber="150">
                <span class="linked-line" unselectable="on" data-linenumber="150"></span>
              </td>
              <td class="line_content">
</td>
            </tr>
            <tr class="line_holder" id="L151">
              <td class="line-num" data-linenumber="151">
                <span class="linked-line" unselectable="on" data-linenumber="151"></span>
              </td>
              <td class="line_content">If an account status is red, you can disable (undeploy) and enable (deploy) module again. This usually helps with any
</td>
            </tr>
            <tr class="line_holder" id="L152">
              <td class="line-num" data-linenumber="152">
                <span class="linked-line" unselectable="on" data-linenumber="152"></span>
              </td>
              <td class="line_content">transient issues during account creation.
</td>
            </tr>
            <tr class="line_holder" id="L153">
              <td class="line-num" data-linenumber="153">
                <span class="linked-line" unselectable="on" data-linenumber="153"></span>
              </td>
              <td class="line_content">
</td>
            </tr>
            <tr class="line_holder" id="L154">
              <td class="line-num" data-linenumber="154">
                <span class="linked-line" unselectable="on" data-linenumber="154"></span>
              </td>
              <td class="line_content">| <span class="gs">**Manage Account**</span> |
</td>
            </tr>
            <tr class="line_holder" id="L155">
              <td class="line-num" data-linenumber="155">
                <span class="linked-line" unselectable="on" data-linenumber="155"></span>
              </td>
              <td class="line_content">|:--:| 
</td>
            </tr>
            <tr class="line_holder" id="L156">
              <td class="line-num" data-linenumber="156">
                <span class="linked-line" unselectable="on" data-linenumber="156"></span>
              </td>
              <td class="line_content">| !<span class="p">[</span><span class="nv">Troubleshooting Account 1/3</span><span class="p">](</span><span class="sx">images/manage_account_1.png</span><span class="p">)</span> | 
</td>
            </tr>
            <tr class="line_holder" id="L157">
              <td class="line-num" data-linenumber="157">
                <span class="linked-line" unselectable="on" data-linenumber="157"></span>
              </td>
              <td class="line_content">
</td>
            </tr>
            <tr class="line_holder" id="L158">
              <td class="line-num" data-linenumber="158">
                <span class="linked-line" unselectable="on" data-linenumber="158"></span>
              </td>
              <td class="line_content"><span class="p">***</span>
</td>
            </tr>
            <tr class="line_holder" id="L159">
              <td class="line-num" data-linenumber="159">
                <span class="linked-line" unselectable="on" data-linenumber="159"></span>
              </td>
              <td class="line_content">
</td>
            </tr>
            <tr class="line_holder" id="L160">
              <td class="line-num" data-linenumber="160">
                <span class="linked-line" unselectable="on" data-linenumber="160"></span>
              </td>
              <td class="line_content">| <span class="gs">**Undeploy module**</span> |
</td>
            </tr>
            <tr class="line_holder" id="L161">
              <td class="line-num" data-linenumber="161">
                <span class="linked-line" unselectable="on" data-linenumber="161"></span>
              </td>
              <td class="line_content">|:--:| 
</td>
            </tr>
            <tr class="line_holder" id="L162">
              <td class="line-num" data-linenumber="162">
                <span class="linked-line" unselectable="on" data-linenumber="162"></span>
              </td>
              <td class="line_content">| !<span class="p">[</span><span class="nv">Troubleshooting Account 2/3</span><span class="p">](</span><span class="sx">images/manage_account_2.png</span><span class="p">)</span> | 
</td>
            </tr>
            <tr class="line_holder" id="L163">
              <td class="line-num" data-linenumber="163">
                <span class="linked-line" unselectable="on" data-linenumber="163"></span>
              </td>
              <td class="line_content">
</td>
            </tr>
            <tr class="line_holder" id="L164">
              <td class="line-num" data-linenumber="164">
                <span class="linked-line" unselectable="on" data-linenumber="164"></span>
              </td>
              <td class="line_content"><span class="p">***</span>
</td>
            </tr>
            <tr class="line_holder" id="L165">
              <td class="line-num" data-linenumber="165">
                <span class="linked-line" unselectable="on" data-linenumber="165"></span>
              </td>
              <td class="line_content">
</td>
            </tr>
            <tr class="line_holder" id="L166">
              <td class="line-num" data-linenumber="166">
                <span class="linked-line" unselectable="on" data-linenumber="166"></span>
              </td>
              <td class="line_content">| <span class="gs">**Deploy module**</span> |
</td>
            </tr>
            <tr class="line_holder" id="L167">
              <td class="line-num" data-linenumber="167">
                <span class="linked-line" unselectable="on" data-linenumber="167"></span>
              </td>
              <td class="line_content">|:--:| 
</td>
            </tr>
            <tr class="line_holder" id="L168">
              <td class="line-num" data-linenumber="168">
                <span class="linked-line" unselectable="on" data-linenumber="168"></span>
              </td>
              <td class="line_content">| !<span class="p">[</span><span class="nv">Troubleshooting Account 3/3</span><span class="p">](</span><span class="sx">images/manage_account_3.png</span><span class="p">)</span> | 
</td>
            </tr>
            <tr class="line_holder" id="L169">
              <td class="line-num" data-linenumber="169">
                <span class="linked-line" unselectable="on" data-linenumber="169"></span>
              </td>
              <td class="line_content">
</td>
            </tr>
            <tr class="line_holder" id="L170">
              <td class="line-num" data-linenumber="170">
                <span class="linked-line" unselectable="on" data-linenumber="170"></span>
              </td>
              <td class="line_content"><span class="p">***</span>
</td>
            </tr>
            <tr class="line_holder" id="L171">
              <td class="line-num" data-linenumber="171">
                <span class="linked-line" unselectable="on" data-linenumber="171"></span>
              </td>
              <td class="line_content">
</td>
            </tr>
            <tr class="line_holder" id="L172">
              <td class="line-num" data-linenumber="172">
                <span class="linked-line" unselectable="on" data-linenumber="172"></span>
              </td>
              <td class="line_content">
</td>
            </tr>
            <tr class="line_holder" id="L173">
              <td class="line-num" data-linenumber="173">
                <span class="linked-line" unselectable="on" data-linenumber="173"></span>
              </td>
              <td class="line_content"><span class="gu">### Export account details</span>
</td>
            </tr>
            <tr class="line_holder" id="L174">
              <td class="line-num" data-linenumber="174">
                <span class="linked-line" unselectable="on" data-linenumber="174"></span>
              </td>
              <td class="line_content">
</td>
            </tr>
            <tr class="line_holder" id="L175">
              <td class="line-num" data-linenumber="175">
                <span class="linked-line" unselectable="on" data-linenumber="175"></span>
              </td>
              <td class="line_content">| <span class="gs">**Export accounts details**</span> |
</td>
            </tr>
            <tr class="line_holder" id="L176">
              <td class="line-num" data-linenumber="176">
                <span class="linked-line" unselectable="on" data-linenumber="176"></span>
              </td>
              <td class="line_content">|:--:| 
</td>
            </tr>
            <tr class="line_holder" id="L177">
              <td class="line-num" data-linenumber="177">
                <span class="linked-line" unselectable="on" data-linenumber="177"></span>
              </td>
              <td class="line_content">| !<span class="p">[</span><span class="nv">Export accounts details</span><span class="p">](</span><span class="sx">images/export_account.png</span><span class="p">)</span> | 
</td>
            </tr>
            <tr class="line_holder" id="L178">
              <td class="line-num" data-linenumber="178">
                <span class="linked-line" unselectable="on" data-linenumber="178"></span>
              </td>
              <td class="line_content">
</td>
            </tr>
            <tr class="line_holder" id="L179">
              <td class="line-num" data-linenumber="179">
                <span class="linked-line" unselectable="on" data-linenumber="179"></span>
              </td>
              <td class="line_content"><span class="p">***</span>
</td>
            </tr>
            <tr class="line_holder" id="L180">
              <td class="line-num" data-linenumber="180">
                <span class="linked-line" unselectable="on" data-linenumber="180"></span>
              </td>
              <td class="line_content">
</td>
            </tr>
            <tr class="line_holder" id="L181">
              <td class="line-num" data-linenumber="181">
                <span class="linked-line" unselectable="on" data-linenumber="181"></span>
              </td>
              <td class="line_content"><span class="gu">### Terminate Event</span>
</td>
            </tr>
            <tr class="line_holder" id="L182">
              <td class="line-num" data-linenumber="182">
                <span class="linked-line" unselectable="on" data-linenumber="182"></span>
              </td>
              <td class="line_content">
</td>
            </tr>
            <tr class="line_holder" id="L183">
              <td class="line-num" data-linenumber="183">
                <span class="linked-line" unselectable="on" data-linenumber="183"></span>
              </td>
              <td class="line_content"><span class="gt">&gt; Always remember to terminate event on completion.</span>
</td>
            </tr>
            <tr class="line_holder" id="L184">
              <td class="line-num" data-linenumber="184">
                <span class="linked-line" unselectable="on" data-linenumber="184"></span>
              </td>
              <td class="line_content">
</td>
            </tr>
            <tr class="line_holder" id="L185">
              <td class="line-num" data-linenumber="185">
                <span class="linked-line" unselectable="on" data-linenumber="185"></span>
              </td>
              <td class="line_content">| <span class="gs">**Terminate Event**</span> |
</td>
            </tr>
            <tr class="line_holder" id="L186">
              <td class="line-num" data-linenumber="186">
                <span class="linked-line" unselectable="on" data-linenumber="186"></span>
              </td>
              <td class="line_content">|:--:| 
</td>
            </tr>
            <tr class="line_holder" id="L187">
              <td class="line-num" data-linenumber="187">
                <span class="linked-line" unselectable="on" data-linenumber="187"></span>
              </td>
              <td class="line_content">| !<span class="p">[</span><span class="nv">Terminate Event</span><span class="p">](</span><span class="sx">images/terminate_event.png</span><span class="p">)</span> | 
</td>
            </tr>
        </tbody>
      </table>
    </div>

</div>
</div>


</div>
<nav class='navbar navbar-default footer' role='navigation'>
<footer class='footer top-buffer' id='footer'>
<div class='col-sm-9 col-md-8 main'>
<h3>Packages</h3>
<ul class='unstyled'>
<li><a href="https://octane.amazon.com/package">Create Package</a></li>
<li><a href="/packages/find_by_team_for_user">All packages for my team</a></li>
</ul>
<h3>Commit Notifications</h3>
<ul class='unstyled'>
<li><a href="https://w.amazon.com/index.php/BuilderTools/Product/RevisionControl/CommitNotifications">RSS</a></li>
<li><a href="/commit-notifications">Email</a></li>
</ul>
</div>
<div class='col-sm-3 col-md-4 sidebar'>
<div class='business_card clearfix'>
<h3>Need help?</h3>
<ul class='unstyled'>
<li><a target="_blank" href="https://tiny.amazon.com/1bxu90lx3/codeacbug">Submit an Issue (problems or suggestions)</a></li>
<li><a target="_blank" href="https://w.amazon.com/index.php/BuilderTools/Product/CodeBrowser">Code Browser Documentation</a></li>
<li><a target="_blank" href="https://w.amazon.com/index.php/BuilderTools/Product/CodeBrowser/CRUX">CRUX Documentation</a></li>
<li><a target="_blank" href="https://w.amazon.com/index.php/BuilderTools/Product/CodeSearch/User%20Guide">Code Search Documentation</a></li>
<li><a target="_blank" href="https://w.amazon.com/index.php/DTUX/Browser_Support_Policy">Browser Support Policy</a></li>
</ul>
</div>
</div>
</footer>
</nav>

<script>
  var codeBrowserSpoofedUser = "jalawala"
</script>
<script src="https://internal-cdn.amazon.com/code.amazon.com/pub/assets/cdn/vendor-part1-92632069e516323f9321984264819d16126dfe013a84267ba90241da0f10db5f.js"></script>
<script src="https://internal-cdn.amazon.com/code.amazon.com/pub/assets/cdn/vendor-part2-b949a32ba4ecf65053b6db63159faeaa9e70b1aadf5b6db628a05310036fce8c.js"></script>
<script src="https://internal-cdn.amazon.com/code.amazon.com/pub/assets/cdn/vendor-part3-1dfdd1d214d96620416147c5070a1ed8aeffa31bfe6fdc265904c106aa1a5aa5.js"></script>
<script src="https://internal-cdn.amazon.com/code.amazon.com/pub/assets/cdn/vendor-part4-caf29714919a9cb48d6e2db3958aac4e4a8191d430466fc96629c855695d004c.js"></script>
<script src="https://internal-cdn.amazon.com/code.amazon.com/pub/assets/cdn/application-73163c677686ba6b4840d7047d062adc4fadd006dc4b46ecace73788a8c1907c.js"></script>
<script src="https://internal-cdn.amazon.com/is-it-down.amazon.com/javascripts/stripe.min.js"></script>
<script>
  (function() {
    if (typeof isItDownStripe === 'function') {
      $(function() {
        return isItDownStripe('sourcecode', 1107, 1);
      });
    }
  
  }).call(this);
</script>
<script src="https://internal-cdn.amazon.com/code.amazon.com/pub/assets/cdn/application_angular-6113186e56d0ff92d345189173d89ee99a3b66149d33916b304771a9e2603e37.js"></script>
<script>
  bootstrapNgApp('code-browser', 'markdown');
</script>
<script>
  $(document).ready(function() {
      $('#branches').select2({
          width: "274px",
          data: [{"text":"Official Branches","children":[{"text":"mainline (default)","id":"/packages/Containers-immersionday-workshop/blobs/heads/mainline/--/README.md"}]}],
          createSearchChoice: function(term, data) {
            if ($(data).filter(function() { return this.text.localeCompare(term)===0; }).length===0) {
              // This code fires if the user enters a string and hits return (rather than selecting the item
              // from the dropdown.  This breaks when viewing commits (logs). Customize it accordingly.
              if ('/packages/Containers-immersionday-workshop/blobs/'.match(/\/logs/)) {
                var id_string = '/packages/Containers-immersionday-workshop/blobs//' + term;
                if ('README.md') {
                  id_string += '/--/README.md';
                }
                return {text:term, id: id_string};
              }
              return {text:term, id:'/packages/Containers-immersionday-workshop/blobs/' + term + '/--/README.md'};
            }
          },
      });
      $('#branches').select2('data', null);
      $('#branches').change(function() {
        document.location = $(this).val();
      });
  });
</script>
<script>
  (function() {
    $(function() {
      return $('.add_relation_link a').click(function() {
        $('.add_related_items').show(500).find('input[name=relation]').delay(500).focus();
        $(this).hide();
        return false;
      });
    });
  
  }).call(this);
</script>
<script>
  (function() {
    $(function() {
      return $('.commit-see-more').click(function() {
        $('.commit-see-more').text($('.commit-see-more').text() === 'see more' ? 'see less' : 'see more');
        $('.last-commit-summary, .commit_header').toggle();
        return false;
      });
    });
  
  }).call(this);
</script>
<script>
  (function() {
    $('li.permalink a').click(function() {
      window.location.href = this.href + location.hash;
      return false;
    });
  
  }).call(this);
</script>
<script>
  (function() {
    var relatedItems;
  
    relatedItems = new Codac.RelatedItemsModel("Containers-immersionday-workshop", "c561dea942838bc0e25029134936a482af94a5da", 'mainline', '');
  
    Codac.model.relatedItemsModel(relatedItems);
  
  }).call(this);
</script>
<script>
  (function() {
    var onUrlChange, premalinkBtnEl, premalinkPath;
  
    (function() {
      var anchor, anchorMatch, hash, hl_lines_match, path, ranges, search;
      anchor = window.location.hash.split('#')[1] || '';
      anchorMatch = anchor.match(/^line-(\d+)/);
      if (anchorMatch) {
        anchor = 'L' + anchorMatch[1];
      }
      search = window.location.search;
      hl_lines_match = search.match(/hl_lines=([\d\-\,]+)/);
      ranges = '';
      if (hl_lines_match) {
        ranges = hl_lines_match[1].split(',').map(function(range) {
          return range.split('-').map(function(lineNum) {
            return 'L' + lineNum;
          }).join('-');
        }).join(',');
      }
      hash = ranges;
      if (anchorMatch) {
        hash += '|' + anchor;
      }
      if (hash !== '') {
        if (hash !== '') {
          window.location.hash = '#' + hash;
        }
        path = window.location.pathname + window.location.hash;
        return window.history.pushState(void 0, void 0, path);
      }
    })();
  
    premalinkBtnEl = $('#file_actions .permalink');
  
    premalinkPath = premalinkBtnEl.find('.minibutton').attr('href');
  
    onUrlChange = function() {
      return premalinkBtnEl.hide();
    };
  
    setTimeout((function() {
      return (new Diff()).enableHighlighting({
        basePath: premalinkPath,
        onUrlChange: onUrlChange
      });
    }), 0);
  
  }).call(this);
</script>
<script>
  (function() {
    $(function() {
      return $('.navbar-search.navbar-form').submit(function() {
        $(this).submit(function(e) {
          e.preventDefault();
          return false;
        });
        return $('.search-spinner').show();
      });
    });
  
  }).call(this);
</script>

</body>
</html>
