files = [
    """
        Organizing your CSS
        Previous
        Overview: CSS building blocks
        Next
        As you start to work on larger stylesheets and big projects you will discover that maintaining a huge CSS file can be challenging. In this article we will take a brief look at some best practices for writing your CSS to make it easily maintainable, and some of the solutions you will find in use by others to help improve maintainability.

        Prerequisites:	Basic software installed, basic knowledge of working with files, HTML basics (study Introduction to HTML), and an idea of how CSS works (study CSS first steps.)
        Objective:	To learn some tips and best practices for organizing stylesheets, and find out about some of the naming conventions and tools in common usage to help with CSS organization and team working.
        Tips to keep your CSS tidy
        Here are some general suggestions for ways to keep your stylesheets organized and tidy.

        Does your project have a coding style guide?
        If you are working with a team on an existing project, the first thing to check is whether the project has an existing style guide for CSS. The team style guide should always win over your own personal preferences. There often isn't a right or wrong way to do things, but consistency is important.

        For example, have a look at the CSS guidelines for MDN code examples.

        Keep it consistent
        If you get to set the rules for the project or are working alone, then the most important thing to do is to keep things consistent. Consistency can be applied in all sorts of ways, such as using the same naming conventions for classes, choosing one method of describing color, or maintaining consistent formatting. (For example, will you use tabs or spaces to indent your code? If spaces, how many spaces?)

        Having a set of rules you always follow reduces the amount of mental overhead needed when writing CSS, as some of the decisions are already made.

        Formatting readable CSS
        There are a couple of ways you will see CSS formatted. Some developers put all of the rules onto a single line, like so:

        css
        Copy to Clipboard
        .box {background-color: #567895; }
        h2 {background-color: black; color: white; }
        Other developers prefer to break everything onto a new line:

        css
        Copy to Clipboard
        .box {
        background-color: #567895;
        }

        h2 {
        background-color: black;
        color: white;
        }
        CSS doesn't mind which one you use. We personally find it is more readable to have each property and value pair on a new line.

        Comment your CSS
        Adding comments to your CSS will help any future developer work with your CSS file, but will also help you when you come back to the project after a break.

        css
        Copy to Clipboard
        /* This is a CSS comment
        It can be broken onto multiple lines. */
        A good tip is to add a block of comments between logical sections in your stylesheet too, to help locate different sections quickly when scanning it, or even to give you something to search for to jump right into that part of the CSS. If you use a string that won't appear in the code, you can jump from section to section by searching for it — below we have used ||.

        css
        Copy to Clipboard
        /* || General styles */

        /* … */

        /* || Typography */

        /* … */

        /* || Header and Main Navigation */

        /* … */
        You don't need to comment every single thing in your CSS, as much of it will be self-explanatory. What you should comment are the things where you made a particular decision for a reason.

        You may have used a CSS property in a specific way to get around older browser incompatibilities, for example:

        css
        Copy to Clipboard
        .box {
        background-color: red; /* fallback for older browsers that don't support gradients */
        background-image: linear-gradient(to right, #ff0000, #aa0000);
        }
        Perhaps you followed a tutorial to achieve something, and the CSS isn't very self-explanatory or recognizable. In that case, you could add the URL of the tutorial to the comments. You will thank yourself when you come back to this project in a year or so and can vaguely remember that there was a great tutorial about that thing, but can't recall where it's from.

        Create logical sections in your stylesheet
        It is a good idea to have all of the common styling first in the stylesheet. This means all of the styles which will generally apply unless you do something special with that element. You will typically have rules set up for:

        body
        p
        h1, h2, h3, h4, h5
        ul and ol
        The table properties
        Links
        In this section of the stylesheet we are providing default styling for the type on the site, setting up a default style for data tables and lists and so on.

        css
        Copy to Clipboard
        /* || GENERAL STYLES */

        body {
        /* … */
        }

        h1,
        h2,
        h3,
        h4 {
        /* … */
        }

        ul {
        /* … */
        }

        blockquote {
        /* … */
        }
        After this section, we could define a few utility classes, for example, a class that removes the default list style for lists we're going to display as flex items or in some other way. If you have a few styling choices you know you will want to apply to lots of different elements, they can be put in this section.

        css
        Copy to Clipboard
        /* || UTILITIES */

        .no-bullets {
        list-style: none;
        margin: 0;
        padding: 0;
        }

        /* … */
        Then we can add everything that is used sitewide. That might be things like the basic page layout, the header, navigation styling, and so on.

        css
        Copy to Clipboard
        /* SITEWIDE */

        .main-nav {
        /* … */
        }

        .logo {
        /* … */
        }
        Finally, we will include CSS for specific things, broken down by the context, page, or even component in which they are used.

        css
        Copy to Clipboard
        /* || STORE PAGES */

        .product-listing {
        /* … */
        }

        .product-box {
        /* … */
        }
        By ordering things in this way, we at least have an idea in which part of the stylesheet we will be looking for something that we want to change.

        Avoid overly-specific selectors
        If you create very specific selectors, you will often find that you need to duplicate chunks of your CSS to apply the same rules to another element. For example, you might have something like the selector below, which applies the rule to a <p> with a class of box inside an <article> with a class of main.

        css
        Copy to Clipboard
        article.main p.box {
        border: 1px solid #ccc;
        }
        If you then wanted to apply the same rules to something outside of main, or to something other than a <p>, you would have to add another selector to these rules or create a whole new ruleset. Instead, you could use the selector .box to apply your rule to any element that has the class box:

        css
        Copy to Clipboard
        .box {
        border: 1px solid #ccc;
        }
        There will be times when making something more specific makes sense; however, this will generally be an exception rather than usual practice.

        Break large stylesheets into multiple smaller ones
        In cases where you have very different styles for distinct parts of the site, you might want to have one stylesheet that includes all the global rules, as well as some smaller stylesheets that include the specific rules needed for those sections. You can link to multiple stylesheets from one page, and the normal rules of the cascade apply, with rules in stylesheets linked later coming after rules in stylesheets linked earlier.

        For example, we might have an online store as part of the site, with a lot of CSS used only for styling the product listings and forms needed for the store. It would make sense to have those things in a different stylesheet, only linked to on store pages.

        This can make it easier to keep your CSS organized, and also means that if multiple people are working on the CSS, you will have fewer situations where two people need to work on the same stylesheet at once, leading to conflicts in source control.

        Other tools that can help
        CSS itself doesn't have much in the way of in-built organization; therefore, the level of consistency in your CSS will largely depend on you. The web community has developed various tools and approaches that can help you to manage larger CSS projects. Since you are likely to come across these aids when working with other people, and since they are often of help generally, we've included a short guide to some of them.

        CSS methodologies
        Instead of needing to come up with your own rules for writing CSS, you may benefit from adopting one of the approaches already designed by the community and tested across many projects. These methodologies are essentially CSS coding guides that take a very structured approach to writing and organizing CSS. Typically they tend to render CSS more verbosely than you might have if you wrote and optimized every selector to a custom set of rules for that project.

        However, you do gain a lot of structure by adopting one. Since many of these systems are widely used, other developers are more likely to understand the approach you are using and be able to write their own CSS in the same way, rather than having to work out your own personal methodology from scratch.

        OOCSS
        Most of the approaches you will encounter owe something to the concept of Object Oriented CSS (OOCSS), an approach made popular by the work of Nicole Sullivan. The basic idea of OOCSS is to separate your CSS into reusable objects, which can be used anywhere you need on your site. The standard example of OOCSS is the pattern described as The Media Object. This is a pattern with a fixed size image, video or other element on one side, and flexible content on the other. It's a pattern we see all over websites for comments, listings, and so on.

        If you are not taking an OOCSS approach you might create a custom CSS for the different places this pattern is used, for example, by creating two classes, one called comment with a bunch of rules for the component parts, and another called list-item with almost the same rules as the comment class except for some tiny differences. The differences between these two components are the list-item has a bottom border, and images in comments have a border whereas list-item images do not.

        css
        Copy to Clipboard
        .comment {
        display: grid;
        grid-template-columns: 1fr 3fr;
        }

        .comment img {
        border: 1px solid grey;
        }

        .comment .content {
        font-size: 0.8rem;
        }

        .list-item {
        display: grid;
        grid-template-columns: 1fr 3fr;
        border-bottom: 1px solid grey;
        }

        .list-item .content {
        font-size: 0.8rem;
        }
        In OOCSS, you would create one pattern called media that would have all of the common CSS for both patterns — a base class for things that are generally the shape of the media object. Then we'd add an additional class to deal with those tiny differences, thus extending that styling in specific ways.

        css
        Copy to Clipboard
        .media {
        display: grid;
        grid-template-columns: 1fr 3fr;
        }

        .media .content {
        font-size: 0.8rem;
        }

        .comment img {
        border: 1px solid grey;
        }

        .list-item {
        border-bottom: 1px solid grey;
        }
        In your HTML, the comment would need both the media and comment classes applied:

        html
        Copy to Clipboard
        <div class="media comment">
        <img src="" alt="" />
        <div class="content"></div>
        </div>
        The list-item would have media and list-item applied:

        html
        Copy to Clipboard
        <ul>
        <li class="media list-item">
            <img src="" alt="" />
            <div class="content"></div>
        </li>
        </ul>
        The work that Nicole Sullivan did in describing this approach and promoting it means that even people who are not strictly following an OOCSS approach today will generally be reusing CSS in this way — it has entered our understanding as a good way to approach things in general.

        BEM
        BEM stands for Block Element Modifier. In BEM a block is a stand-alone entity such as a button, menu, or logo. An element is something like a list item or a title that is tied to the block it is in. A modifier is a flag on a block or element that changes the styling or behavior. You will be able to recognize code that uses BEM due to the extensive use of dashes and underscores in the CSS classes. For example, look at the classes applied to this HTML from the page about BEM Naming conventions:

        html
        Copy to Clipboard
        <form class="form form--theme-xmas form--simple">
        <label class="label form__label" for="inputId"></label>
        <input class="form__input" type="text" id="inputId" />

        <input
            class="form__submit form__submit--disabled"
            type="submit"
            value="Submit" />
        </form>
        The additional classes are similar to those used in the OOCSS example; however, they use the strict naming conventions of BEM.

        BEM is widely used in larger web projects and many people write their CSS in this way. It is likely that you will come across examples, even in tutorials, that use BEM syntax, without mentioning why the CSS is structured in such a way.

        Read more about this system BEM 101 on CSS Tricks.

        Other common systems
        There are a large number of these systems in use. Other popular approaches include Scalable and Modular Architecture for CSS (SMACSS), created by Jonathan Snook, ITCSS from Harry Roberts, and Atomizer CSS (ACSS), originally created by Yahoo!. If you come across a project that uses one of these approaches, then the advantage is that you will be able to search and find many articles and guides to help you understand how to code in the same style.

        The disadvantage of using such a system is that they can seem overly complex, especially for smaller projects.

        Build systems for CSS
        Another way to organize CSS is to take advantage of some of the tooling that is available for front-end developers, which allows you to take a slightly more programmatic approach to writing CSS. There are a number of tools, which we refer to as pre-processors and post-processors. A pre-processor runs over your raw files and turns them into a stylesheet, whereas a post-processor takes your finished stylesheet and does something to it — perhaps to optimize it in order that it will load faster.

        Using any of these tools will require that your development environment be able to run the scripts that do the pre- and post-processing. Many code editors can do this for you, or you can install command line tools to help.

        The most popular pre-processor is Sass. This is not a Sass tutorial, so I will briefly explain a couple of the things that Sass can do, which are really helpful in terms of organization even if you don't use any of the other Sass features. If you want to learn a lot more about Sass, start with the Sass basics article, then move on to their other documentation.

        Defining variables
        CSS now has native custom properties, making this feature increasingly less important. However, one of the reasons you might use Sass is to be able to define all of the colors and fonts used in a project as settings, then to use that variable around the project. This means that if you realize you have used the wrong shade of blue, you only need change it in one place.

        If we created a variable called $base-color, as in the first line below, we could then use it through the stylesheet anywhere that required that color.

        scss
        Copy to Clipboard
        $base-color: #c6538c;

        .alert {
        border: 1px solid $base-color;
        }
        Once compiled to CSS, you would end up with the following CSS in the final stylesheet.

        css
        Copy to Clipboard
        .alert {
        border: 1px solid #c6538c;
        }
        Compiling component stylesheets
        I mentioned above that one way to organize CSS is to break down stylesheets into smaller stylesheets. When using Sass you can take this to another level and have lots of very small stylesheets — even going as far as having a separate stylesheet for each component. By using the included functionality in Sass (partials), these can all be compiled together into one or a small number of stylesheets to actually link into your website.

        So, for example, with partials, you could have several style files inside a directory, say foundation/_code.scss, foundation/_lists.scss, foundation/_footer.scss, foundation/_links.scss, etc. You could then use the Sass @use rule to load them into other stylesheets:

        scss
        Copy to Clipboard
        // foundation/_index.scss
        @use "code";
        @use "lists";
        @use "footer";
        @use "links";
        If the partials are all loaded into an index file, as implied above, you can then load that entire directory into another stylesheet in one go:

        scss
        Copy to Clipboard
        // style.scss
        @use "foundation";
        Note: A simple way to try out Sass is to use CodePen — you can enable Sass for your CSS in the Settings for a Pen, and CodePen will then run the Sass parser for you in order that you can see the resulting webpage with regular CSS applied. Sometimes you will find that CSS tutorials have used Sass rather than plain CSS in their CodePen demos, so it is handy to know a little bit about it.

        Post-processing for optimization
        If you are concerned about adding size to your stylesheets, for example, by adding a lot of additional comments and whitespace, then a post-processing step could be to optimize the CSS by stripping out anything unnecessary in the production version. An example of a post-processor solution for doing this would be cssnano.

        Summary
        This is the final part of our building blocks module, and as you can see there are many ways in which your exploration of CSS can continue from this point — but now you can go on to testing yourself with our assessments: the first one is linked below.

        To learn more about layout in CSS, see the CSS Layout module.

        You should also now have the skills to explore the rest of the MDN CSS material. You can look up properties and values, explore our CSS Cookbook for patterns to use, or continue reading in some of the specific guides, such as our Guide to CSS grid layout.
    """,
    """
        Recipe: Media objects
        The Media Object is a pattern we see all over the web. It refers to a two-column box with an image on one side and descriptive text on the other, e.g. a social media post.

        Example of a media object with profile image on the left side and lorem ipsum text to the right filling up 80% of the space

        Requirements
        Media Object pattern needs some or all of the following characteristics:

        @media (min-width: 500px) {
        .media {
            display: grid;
            grid-template-columns: fit-content(200px) 1fr;
            grid-template-rows:1fr auto;
            grid-template-areas:
            "image content"
            "image footer";
            grid-gap: 20px;
            margin-bottom: 4em;
        }

        .media-flip {
            grid-template-columns: 1fr fit-content(250px);
            grid-template-areas:
            "content image"
            "footer image";
        }

        .img {
            grid-area: image;
        }

        .content {
            grid-area: content;
        }

        .footer {
            grid-area: footer;
        }

        }

        Choices made
        I have chosen to use grid layout for the media object as it allows me to control the layout in two dimensions when I need to. This means that when we have a footer, with short content above, the footer can be pushed down to the bottom of the media object.

        Another reason to use grid layout is in order that I can use fit-content for the track sizing of the image. By using fit-content with a maximum size of 200 pixels, when we have a small image such as the icon, the track only gets as large as the size of that image — the max-content size. If the image is larger, the track stops growing at 200 pixels and as the image has a max-width of 100% applied, it scales down so that it continues to fit inside the column.

        By using grid-template-areas to achieve the layout, I can see the pattern in the CSS. I define my grid once we have a max-width of 500 pixels, so on smaller devices the media object stacks.

        An option for the pattern is to flip it to switch the image to the other side — this is done by adding the media-flip class, which defines a flipped grid template causing the layout to be mirrored.

        When we nest one media object inside another we need to place it into the second track in the regular layout, and the first track when flipped.

        Column layouts
        You will often need to create a layout which has a number of columns, and CSS provides several ways to do this. Whether you use Multi-column, Flexbox, or Grid layout will depend on what you are trying to achieve, and in this recipe we explore these options.

        three different styles of layouts which have two columns in the container.

        Requirements
        There are a number of design patterns you might want to achieve with your columns:

        A continuous thread of content broken up into newspaper-style columns.
        A single row of items arranged as columns, with all heights being equal.
        Multiple rows of columns lined up by row and column.
        The recipes
        You need to choose different layout methods in order to achieve your requirements.

        A continuous thread of content — multi-column layout
        If you create columns using multi-column layout your text will remain as a continuous stream filling each column in turn. The columns must all be the same size, and you are unable to target an individual column or the content of an individual column.

        You can control the gaps between columns with the column-gap or gap properties, and add a rule between columns using column-rule.

        .container {
        column-width: 10em;
        column-rule: 1px solid rgb(75 70 74);
        }

        In this example, we used the column-width property to set a minimum width that the columns need to be before the browser adds an additional column. The columns shorthand property can be used to set the column-width and column-count properties, either of which can define the maximum number of columns allowed.

        

        Use multicol when:

        You want your text to display in newspaper-like columns.
        You have a set of small items you want to break into columns.
        You do not need to target individual column boxes for styling.
        A single row of items with equal heights — flexbox
        Flexbox can be used to break content into columns by setting display: flex; to make a parent element a flex-container. Just adding this one property turns all the children (child elements, pseudo-elements, and text nodes) into flex items along a single line. Setting the same flex shorthand property with a single numeric value distributes all the available space equally, generally making all the flex items the same size as long as none have non-wrapping content forcing the item to be larger.

        Margins or the gap property can be used to create gaps between items, but there is currently no CSS property that adds rules between flex items.


        Download this example

        To create a layout with flex items that wrap onto new rows, set the flex-wrap property on the container to wrap. Note that each flex line distributes space for that line only. Items in one line will not necessarily line up with items on other lines, as you'll see in the example below. This is why flexbox is described as one-dimensional. It is designed for controlling layout as a row or a column, but not both at the same time.


        Download this example

        Use flexbox:

        For single rows or columns of items.
        When you want to do alignment on the cross axis after laying out your items.
        When you are happy for wrapped items to share out space along their line only and not line up with items in other lines.
        Lining items up in rows and columns — grid layout
        If you want a two-dimensional grid where items line up in rows and columns, then you should choose CSS grid layout. Similar to how flexbox works on the direct children of the flex container, grid layout works on the direct children of the grid container. Just set display: grid; on the container. Properties set on this container — like grid-template-columns and grid-template-rows — define how the items are distributed along rows and columns.


        Download this example

        Use grid:

        For multiple rows or columns of items.
        When you want to be able to align the items on the block and inline axes.
        When you want items to line up in rows and columns.

        Center an element
        In this recipe, you will see how to center one box inside another by using flexbox and grid. Centering both horizontally and vertically is simple and straightforward.

        an element centered inside a larger box

        Requirements
        To place an item into the center of another box horizontally and vertically.

        Recipe

        .container {
            height: 200px;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .item {
            width: 10em;
        }

        Download this example

        Using flexbox
        To center a box within another box, first turn the containing box into a flex container by setting its display property to flex. Then set align-items to center for vertical centering (on the block axis) and justify-content to center for horizontal centering (on the inline axis). And that's all it takes to center one box inside another!

        HTML
        html
        Copy to Clipboard
        play
        <div class="container">
        <div class="item">I am centered!</div>
        </div>
        CSS
        css
        Copy to Clipboard
        play
        div {
        border: solid 3px;
        padding: 1em;
        max-width: 75%;
        }
        .container {
        display: flex;
        align-items: center;
        justify-content: center;
        height: 8em;
        }
        We set a height for the container to demonstrate that the inner item is indeed vertically centered within the container.

        Result
        play

        Instead of applying align-items: center; on the container, you can also vertically center the inner item by setting align-self to center on the inner item itself.

        Using grid
        Another method you can use for centering one box inside another is to first make the containing box a grid container and then set its place-items property to center to center align its items on both the block and inline axes.

        HTML
        html
        Copy to Clipboard
        play
        <div class="container">
        <div class="item">I am centered!</div>
        </div>
        CSS
        css
        Copy to Clipboard
        play
        div {
        border: solid 3px;
        padding: 1em;
        max-width: 75%;
        }
        .container {
        display: grid;
        place-items: center;
        height: 8em;
        }
        Result
        play

        Instead of applying place-items: center; on the container, you can achieve the same centering by setting place-content: center; on the container or by applying either place-self: center or margin: auto; on the inner item itself.

        Sticky footers
        A sticky footer pattern is one where the footer of your page "sticks" to the bottom of the viewport in cases where the content is shorter than the viewport height. We'll look at a couple of techniques for creating one in this recipe.

        A sticky footer pushed to the bottom of a box

        Requirements
        The Sticky footer pattern needs to meet the following requirements:

        Footer sticks to the bottom of the viewport when content is short.
        If the content of the page extends past the viewport bottom, the footer then sits below the content as normal.
        The recipe

        To take a look at the code, you can download the full example.

        Note: In this example and the following one we are using a wrapper set to min-height: 100%. You can also achieve this for a full page by setting a min-height of 100vh on the <body> and then using it as your grid container.

        Choices made
        In the above example we achieve the sticky footer using CSS grid layout. The .wrapper has a minimum height of 100% which means it is as tall as the container it is in. We then create a single column grid layout with three rows, one row for each part of our layout.

        Grid auto-placement will place our items in source order and so the header goes into the first auto sized track, the main content into the 1fr track and the footer into the final auto sized track. The 1fr track will take up all available space and so grows to fill the gap.

        Alternate method
        You can also use flexbox to create a sticky footer.


        The flexbox example starts out in the same way, but we use display:flex rather than display:grid on the .wrapper; we also set flex-direction to column. Then we set our main content to flex-grow: 1 and the other two elements to flex-shrink: 0 — this prevents them from shrinking smaller when content fills the main area.

        #    Split navigation
        The split navigation is a navigation pattern where one or more elements are separated from the rest of the navigation items.

        Items separated into two groups.

        Requirements
        A common navigation pattern is to have one element pushed away from the others. We can use flexbox to achieve this, without needing to make the two sets of items into two separate flex containers.

        Recipe

        .main-nav {
            display: flex;
            }

            .push {
            margin-left: auto;
            }

        Download this example

        Choices made
        This pattern combines auto margins with flexbox to split the items.

        An auto margin absorbs all available space in the direction it is applied. This is how centering a block with auto margins works — you have a margin on each side of the block trying to take up all of the space, thus pushing the block into the middle.

        In this case the left auto margin takes up any available space and pushes the item over to the right. You could apply the class push to any item in the list.

        #    Breadcrumb navigation
        Breadcrumb navigation helps the user to understand their location in the website by providing a breadcrumb trail back to the start page. The items typically display inline, with a separator between each item, indicating the hierarchy between individual pages.

        Links displayed inline with separators

        Requirements
        Display the hierarchy of the site by displaying inline links, with a separator between the items, indicating the hierarchy between individual pages, with the current page appearing last.

        Recipe

        Download this example

        Note: The example above uses a complex selector to insert content before every li except the last one. This could also be achieved using a complex selector targeting all li elements except the first:

        css
        Copy to Clipboard
        .breadcrumb li:not(:first-child)::before {
        content: "→";
        }
        Feel free to choose the solution that you prefer.

        Choices made
        To display list items inline, we use flexbox layout, thus demonstrating how a line of CSS can give us our navigation. The separators are added using CSS generated content. You could change these to any separator that you like.

        Accessibility concerns
        We used the aria-label and aria-current attributes to help assistive technology users understand what this navigation is and where the current page is in the structure. See the related links for more information.

        Be aware that the separator arrows → added via the content CSS property in the example above are exposed to assistive technologies (AT), including screen readers and braille displays. For a quieter solution, use a decorative <img> in your HTML with an empty alt attribute. An ARIA role set to none or presentation will also prevent the image from being exposed to AT.

        Alternatively, silence the CSS generated content by including an empty string as alternative text, preceded by a slash (/); for example, content: url("arrow.png") / "";.

        If including generated separators that will be exposed to AT, opt for creating the generated content using the ::after pseudo-element selector instead of ::before, so the separator content is announced after the HTML content instead of before it.

        See also
        CSS flexible box layout
        Providing a breadcrumb trail
        Using the aria-current attribute
    """,
    """
        List group with badges
        In this recipe we will create a list group pattern with badges that indicate a count.

        A list of items with a badge indicating a count displayed to the right of the text.

        Requirements
        The list items should be displayed with the badges. The badge should be aligned right and vertically centered. The badge must be centered vertically whether there is a single line of content or multiple lines of text.

        Recipe

        .list-group li {
        display: flex;
        justify-content: space-between;
        align-items: center;
        }

        Download this example

        Choices made
        Flexbox makes this particular pattern straightforward and also facilitates making changes to the layout.

        To ensure the text and badge line up correctly, I use the justify-content property with a value of space-between. This places any extra space between the items. In the live example, if you remove this property, you will see the badge move to the end of the text on items with text shorter than the one line.

        To align the content horizontally, I use the align-items property to align the text and badge on the cross axis. If you want the badge to align to the top of the content instead, change this to align-items: flex-start.
            
        Pagination
        This cookbook pattern demonstrates the navigation pattern used to display pagination, where the user can move between pages of content such as search results.

        Links to sets of pages in a paged listing

        nav {
        display: flex;
        justify-content: center;
        }

        .pagination {
        list-style: none;
        margin: 0;
        padding: 0;
        display: flex;
        }

        .pagination li {
        margin: 0 1px;
        }

        Requirements
        The pagination pattern typically displays items in a row. To ensure that the pagination is understandable by people using a screen reader, we mark the items up as a list inside a <nav> element, and then use CSS to display the layout visually as a row.

        Typically, the pagination component will be centered horizontally underneath the content.

        Card

        This pattern is a list of "card" components with optional footers. A card contains a title, an image, a description or other content, and an attribution or footer. Cards are generally displayed within a group or collection.

        Three card components in a row

        Requirements
        Create a group of cards, with each card component containing a heading, image, content, and, optionally, a footer.

        Each card in the group of cards should be the same height. The optional card footer should stick to the bottom of the card.

        The cards in the group should line up in two dimensions — both vertically and horizontally.

        Recipe


        A short heading
        Hot air balloons
        The idea of reaching the North Pole by means of balloons appears to have been entertained many years ago.

        .cards {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(230px, 1fr));
        grid-gap: 20px;
        }

        .card {
        display: grid;
        grid-template-rows: max-content 200px 1fr;
        }

        .card img {
        object-fit: cover;
        width: 100%;
        height: 100%;
        }


        Grid wrapper
        The grid wrapper pattern is useful for aligning grid content within a central wrapper while also allowing items to break out and align to the edge of the containing element or page.

        Requirements
        Items placed on the grid should be able to align to a horizontally-centered max-width wrapper or the outer edges of the grid, or both.

        Recipe
        .grid {
        display: grid;
        grid-template-columns: minmax(20px, 1fr) repeat(6, minmax(0, 60px)) minmax(20px, 1fr);
        grid-gap: 10px;
        }

        .full-width {
        grid-column: 1 / -1;
        }

        .wrapper {
        grid-column: 2 / -2;
        }

        .left-edge {
        grid-column: 1 / -2;
        }

        .right-wrapper {
        grid-column: 4 / -2;
        }          
    """,
    """
        Cascading Style Sheets (CSS) are the backbone of web design and every front-end developer needs to go through them. Understanding how to wield their power effectively is crucial for creating beautiful, responsive, and maintainable web applications.

        In this guide, we’ll explore some CSS best practices to consider when building applications!


        Before we start, please keep in mind that it is imperative for developers — junior, senior or otherwise — to keep themselves updated on the best practices of whatever technology they’re focusing in. There is nothing preventing the best practices of today changing tomorrow.

        1. Use a CSS Preprocessor
        CSS preprocessors like Sass or Less can help you write more organized and modular code. They offer features like variables, mixins, and nesting, which make your code more maintainable and reduce redundancy.

        2. Organize Your Code
        Organization of code is significantly subjective, but there are general considerations that every developer should keep in mind.

        Use meaningful class and ID names: Choose descriptive class and ID names that reflect the content or purpose of the element. For example, the class definitions in <li className="navbar-link admin-link"> clearly refects that it’s a link in the navigation bar and that it’s a link that only admin users would see in the UI.
        Use consistent naming conventions: Stick to a naming convention for your CSS class and ID definitions. Doing so will allow development teams to maintain consistency and improve legibility across their projects. BEM, OOCSS and SMACSS are popular and well documented naming conventions. Alternatively, you can always use a customized naming convention that fits your needs, so long as you adhere to it.
        3. Optimize your selector definitions
        CSS selectors are used to locate the HTML elements you want to style. There are multiple ways to use selectors, which you can reference here.

        In general, you want to avoid using overly specific selectors that are too tightly coupled to the HTML structure. This can make your CSS hard to maintain. For example:

        div#container > ul.navigation li.active a.btn-primary span.icon {
        /* CSS rules */
        }
        While this selector may work for the specific element you have in mind, it’s excessively specific. If any changes are made to the HTML structure, such as adding new elements or reordering them, this selector is likely to break. Instead, favor more flexible selectors, for example:

        .nav-link {
        /* CSS rules for navigation links */
        }
        In this example, we’re using a class-based selector that targets all navigation links. This is more maintainable and less prone to breaking if the HTML structure changes.

        4. Understand CSS specificity rules
        Specificity is an internal calculation used by browsers to determine the CSS declaration that is the most relevant to an element and determines the property value to apply to that element.

        Understanding how CSS specificity works allows us to optimize selectors and definitions in the most concise and clear way possible. Consider the following example:

        .container p {
        color: blue;
        }

        .text {
        color: red;
        }
        In the first rule, container p, sets the text color to blue and in the second rule .text, sets the text color to red.

        The rule .container p has a specificity of 0-1-1-0 (one class selector and one type selector). And the rule .text has a specificity of 0-0-1-0 (one class selector).

        The rule with the higher specificity, which is .container p, takes precedence. Therefore, the text inside the <p> element will be blue.

        5. Avoid using the !important property
        Touching upon the last two best practices above is the use of the !important property. You can use it to override ALL previous styling rules for that specific property. For example:

        .myParagraph {
        color: gray;
        }

        p {
        color: red !important;
        }
        In this case, the p tag will have a color of red.

        As a general case, you should avoid using!important too much and rely instead on styling definitions through custom class namings and proper selector definitions.

        The !important property is highly destructive in the sense that it overrides all previous styling for a specific property. As a project’s complexity and size grows, it becomes more difficult to maintain. A destructive definition such as this can be easy to miss and hard to locate when debugging, in addition to potentially introducing side-effects in styling definitions. Be wise about it’s use!

        6. Minimize Nesting
        You shouldn’t nest your CSS selectors too deeply into a single parent, or parent to child relation. Take the following example:

        .wrapper {
        // wrapper styles here
        .container {
            // container styles here
            .card {
            // card styles here
            .content {
                // content styles here
                .paragraph {
                // paragraph styles here
                .paragraph-inner-text {
                    // paragraph-inner-text styles here
                }
                }
            }
            }
        }
        }
        As your project grows and your stylesheet structure along with it, having huge swathes of nestes CSS code becomes difficult to maintain. Deeply nested styles can increase specificity, however, they also make your code harder to read.

        Limit nesting to a reasonable level. Try to avoid nesting selectors more than 3 levels deep.

        7. Modularize Your CSS
        Modularization involves breaking your CSS into small, reusable modules or components. This practice makes your codebase more maintainable and encourages code reusability, especially in larger projects. Each module should encapsulate the styles for a specific UI component or feature.

        For example:

        /* Button Module */
        .button {
        /* Button styles */
        }

        /* Navigation Module */
        .navbar {
        /* Navbar styles */
        }

        /* Card Module */
        .card {
        /* Card styles */
        }
        By organizing your CSS into modules, you can easily reuse the styles for buttons, navigation bars, and cards throughout your website without duplicating code. In addition, if you need to update the styling for a specific component, you can do so in one place, ensuring consistency.

        In larger, more robust architectures, it will be even more efficient to divide your CSS into separate files and directories. A popular pattern to consider is the 7–1 pattern, which relies on Sass.

        8. Responsive Design
        Responsive design is the practice of creating web designs that adapt to different screen sizes and devices. Prioritizing responsive design ensures that an application looks and functions well on a variety of devices, from desktop computers to mobile phones.

        9. Test Across Browsers
        Ensure that your styles work consistently across different browsers by testing and addressing compatibility issues. As a reference, you can use the platform CanIUse to verify if a CSS definition is compatible across all, or at least, a majority of browsers.

        10. Documentation
        Documenting CSS code involves adding comments or creating external documentation that explains the purpose, usage, and important details of your CSS rules and styles.

        Writing documentation is invaluable, especially when working on team projects, or simply when returning to your own code after some time. It is particularly useful in describing the inner functionalities of complex workarounds.

        For more extensive documentation, consider creating a separate document or README file that explains the overall architecture of your CSS, such as naming conventions, and any specific guidelines or considerations for maintaining and extending the styles.

        For example:

        # CSS Documentation

        This document provides an overview of the CSS styles used in our project.

        ## Structure

        Our CSS is organized into the following:

        1. **Components**: Styles related to reusable components, such as forms and buttons.
        2. **Layouts**: Styles for to main page layouts and elements related to layouts, such as containers, grids, headers and footers.

        ## Naming Conventions

        We follow the BEM (Block Element Modifier) naming convention for our classes. For example:
        - `.block` for block-level components.
        - `.block__element` for elements within a block.
        - `.block--modifier` for modifiers that change a block's appearance.

        ## Maintenance Guidelines

        - Avoid excessive nesting to keep our styles maintainable. At most consider 3 levels deep.
    """,
    """
        CSS Best Practices
        This is a guideline of best practices that we can apply to our front-end project. Some of these tips are for CSS pre-processors such as Sass, Less and Stylus. These tips are based on CSS documentation, books, articles and professional experience.

        Table of Contents
        Follow conventions
        Follow a CSS methodology
        Lint the CSS files
        Alphabetize CSS properties
        Cross-browser compatibility
        Prefer CSS over JavaScript
        Comment the CSS
        Avoid undoing styles
        Avoid magic numbers
        Avoid qualified selectors
        Avoid hard-coded values
        Avoid brute forcing
        Avoid dangerous selectors
        Avoid extra selectors
        Avoid reactive !important
        Avoid IDs
        Avoid loose class names
        Avoid string concatenation for classes
        Avoid duplicated key selectors
        Avoid using inline styles
        Avoid classes in wrong components
        Avoid @mixin everywhere
        Avoid @extend everywhere
        Avoid shorthand syntax everywhere
        Avoid too many font files
        Use multiple classes
        Use nested declarations
        Use "Margin: 0 auto" to center layouts
        Use Hex Code instead of Name Color
        Use a CSS reset
        Use a CSS pre-processor
        Use a CSS post-processor
        Use a CSS framework
        Use a design system
        Use relative units
        Use CSS variables
        Write descriptive media queries
        Understand Block vs Inline Elements
        Separate global vs local style
        Minimize expensive properties
        Style to be responsive or at least adaptive
        Let the content define the size
        Let the parent take care child position
        Keep HTML semantics
        Create the HTML first
        Combine elements with same styles
        Modularize the styles
        Lazy load stylesheets
        Remove unused CSS
        Minimize the CSS
        Follow conventions
        Code conventions are base rules that allow the creation of a uniform code base across an organization. Following them does not only increase the uniformity and therefore the quality of the code. Airbnb CSS/Sass Style Guide is very popular and recommended. We can complete them with CSS Guidelines and Sass Guidelines. To make it mandatory, we need a linter, formatter and strong code review. The code conventions must be dynamic and adaptable for each team and project. It is up to each team to define its convention. Finally, take a few minutes to browse Awesome Sass. Awesome Sass is a list of awesome Sass and SCSS frameworks, libraries, style guides, articles, and resources.

        Follow a CSS methodology
        CSS methodologies will ensure consistency and future proof our styles. There are plenty of methodologies out there aiming to reduce the CSS footprint, organize cooperation among programmers and maintain large CSS codebases. BEM (Block, Element, Modifier) was introduced in 2010 as a methodology organized around the idea of dividing the user interface into independent blocks. Other CSS methodologies are ITCSS, OOCSS, SMACSS, SUITCSS and Atomic CSS.

        Lint the CSS files
        Linting works by ensuring that we follow the rules that we define for our style and make sure our styles are consistent, well structured, and follow CSS best practices. We can use stylelint in our CSS projects. It is very well documented and can be integrated with our favorite IDE. To ensure all files committed to git don't have any linting or formatting errors, we can use lint-staged. It allows to run linting commands on files that are staged to be committed.

        Alphabetize CSS properties
        Anyone has their organization rules. However, what makes sense to you is not for another developer. Instead, define your rules, use a linter to enforce the same rules for everyone. Sass Lint and stylelint provide rules to organize our CSS. The specifics of what the linter looks for are up to us, but it can be configured to check everything from syntax errors to making sure our CSS properties are in a strict order.

        Cross-browser compatibility
        Cross-browser compatibility is important. CSS browser prefixes are a way for browser makers to add support for new CSS features before those features are fully supported in all browsers. For example, if we use PostCSS with the Autoprefixer plugin, we can write completely normal CSS without any browser prefixes and let the postprocessor do the rest of the work. Internally, Autoprefixer relies on a library called Browserslist to figure out which browsers to support with prefixing.

        Prefer CSS over JavaScript
        If something we want to do with JavaScript can be done with CSS instead, we use CSS. Before we try to add JavaScript and even when we add JavaScript, we should consider having CSS making the most of the style and using JavaScript for things like triggers and side effects. JavaScript is not fault tolerant. This can be disastrous. We are much more in control when using JavaScript, but we are also much more responsible. In general, our applications are faster using CSS instead of JavaScript.

        Comment the CSS
        One of the best practices that we can implement for CSS code is by putting a comment for each group of CSS code. Just like any other language, it's a great idea to comment our code. Comments are used in CSS to explain a block of code or to make temporary changes during development. The commented code doesn't execute. Regarding comments, we have documentation on how to comment the CSS.

        Avoid undoing styles
        CSS that unsets styles should start ringing alarm bells right away. Rulesets should only ever inherit and add to previous ones, never undo. For more details, see the example below:

        h2 {
        font-size: 2em;
        padding-bottom: 0.5em;
        border-bottom: 1px solid #ccc;
        }

        .no-border {
        padding-bottom: 0;
        border-bottom: none;
        }
        As we go down a stylesheet, we should only ever be adding styles, not taking away. If we are having to undo styling as we go down in the document, is because we started adding too soon. In the example, padding-bottom and border-bottom should be moved from h2 to no-border class.

        Avoid magic numbers
        A magic number is a value that is used because it just works. Magic numbers have several problems associated with them. They soon become out of date, they confuse other developers, they cannot be explained, they cannot be trusted. Never, ever use numbers just because they work.

        Avoid qualified selectors
        Qualified selectors are ones like:

        ul.nav {}

        a.button {}

        div.header {}
        Basically, selectors who are needlessly prepended by an element. These are bad news because they totally inhibit reusability on another element, increase specificity and increase browser workload (decreasing performance). These are all bad traits. Those selectors can, and should be:

        .nav {}

        .button {}

        .header {}
        Which will help us to save actual amounts of code, increase performance, allow greater portability and reduce specificity.

        Avoid hard-coded values
        Not unlike magic numbers, hard-coded values are also bad news. A hard-coded value might be something like this:

        h2 {
        font-size: 24px;
        line-height: 32px;
        }
        line-height: 32px; here is not cool, it should be line-height: 1.333;. Line heights should always be set relatively to make them more forgiving and flexible. This may not seem like a massive difference, but on every text element over a large project, this has a big impact. Hard-coded values are not very future proof, flexible or forgiving, and thus should be avoided.

        Avoid brute forcing
        This one is in a similar vein to hard-coded numbers, but a little more specific. Brute forcing CSS is when we use hard-coded magic numbers and a variety of other techniques to force a layout to work.

        .foo {
        margin-left: -3px;
        }
        This is terrible CSS. This type of CSS is indicative of either a poorly coded layout that requires this kind of manipulation, a lack of understanding of box-model and layout, or both. Well coded layouts should never need brute-forcing, and a solid understanding of box model, layout and looking at our computed styles more often should mean that we'd rarely end up in a situation like this.

        Avoid dangerous selectors
        A dangerous selector is one with far too broad a reach. An obvious and simple example of a dangerous selector might be:

        div {
        background-color: #ffc;
        }
        To give such specific styling to such a generic selector is dangerous. Our styles will leak out into areas they shouldn't as soon as we start trying to use that element again. We'll need to start undoing styles (adding more code to take styles away) in order to combat this.

        Avoid extra selectors
        It's easy to unknowingly add extra selectors to our CSS that clutters the stylesheet. One common example of adding extra selectors is with lists.

        body #container .someclass ul li {}
        In this instance, just the .someclass li would have worked just fine.

        .someclass li {}
        Adding extra selectors won't bring the end of the world, but they do keep our CSS from being as simple and clean as possible.

        Avoid reactive !important
        !important is fine and it's a, well, important tool. However, should only be used in certain circumstances. !important should only ever be used proactively, not reactively. For example, we will always want errors to be red, so this rule is totally fine. Where is bad is when it is used reactively, that is, it's used to get someone out of a specificity problem and force things to work. Using reactively is just a way of circumventing the problems caused by ill-formed CSS. It doesn't fix any problems, it only fixes the symptoms.

        Avoid IDs
        IDs can never be used more than once in a page. IDs can often have their traits abstracted out into many reusable classes. An ID is 255 times more specific than one class or infinitely more specific than a class. They are of no use to anyone and should never be used in CSS.

        Avoid loose class names
        A loose class name is one that is not specific enough to define what is its purpose. For example, imagine a class named .board. Such class name is bad because we can't necessarily glean its purpose based on the class name alone and it is so vague that it might be (accidentally) redefined/reassigned by another developer in a near future. All this can be avoided by using much stricter class names. Classes like .board and .user and suchlike are far too loose, making them hard to quickly understand, and easy to accidentally reuse/override. BEM helps us in this task.

        Avoid string concatenation for classes
        Sass allows us to concatenate strings in our class names with &. The obvious benefit is that we must write our foo namespace only once is certainly very DRY.

        .foo {
        color: red;
        &-bar {
            font-weight: bold;
        }
        }
        One less obvious downside, however, is the fact that the string foo-bar now no longer exists in our source code. Searching our codebase for foo-bar will return only results in HTML. It suddenly became a lot more difficult to locate the source of .foo-bar's styles.

        Avoid duplicated key selectors
        The key selector is the selector that gets targeted/styled. It is often, though not always, the selector just before your opening curly brace.

        header.btn{}

        modal.btn{}

        sidebar.btn{}
        Aside from the fact that a lot of that is just generally pretty poor CSS, the problem is that btn is defined many times. So, there is no Single Source of Truth telling what btn look like and there has been a lot of mutation meaning that the class has many different potential outcomes.

        Avoid using inline styles
        Inline styles are the style attribute in the HTML tags. We should avoid using it because it mixes up content and presentation, which can lead to more trouble. Inline styles are considered as bad practice due to poor scalability and maintainability. It leads to messy code where each HTML file will need to be updated in the event of a style change, instead of a global change in a single external stylesheet. As a rule of thumb, define all styles in the CSS files.

        Avoid classes in wrong components
        If we need to style something differently because of its context, where should we put that additional CSS? In the file that styles the thing? Or in the file that controls that context? We should do our best to group our styles based on the subject (i.e. the key selector). For example, it's much more convenient to have the context of all of our buttons in one place. This makes it much easier to move all of the button styles onto a new project, but more importantly it eases cognitive overhead. You're familiar with the feeling of having ten files open in your text editor whilst just trying to change one small piece of styling. As a simple rule of thumb, ask yourself the question am I styling x or am I styling y? If the answer is _, then your CSS should live in _; if the answer is _, it should live in .xx.cssyy.css.

        Avoid @mixin everywhere
        When we don't have to use mixins, just don't do it. When we use mixins, they have to be well-structured and maintained in a rigorous way. Using mixins for no good reason is the best way to get lost when the project grows. They can cause side effects and become hard to update when they are used in many places. Mixins are here to avoid repeating yourself by keeping a Single Source of Truth. Also, we don't have to use mixins to prefix CSS properties because we have plugins like Autoprefixer.

        Avoid @extend everywhere
        It's not absolutely, always, definitely bad, but it usually is. The problems with @extend are manifold, but to summarize:

        It's actually worse for performance than mixins are;
        It's greedy. Sass will @extend every instance of a class that it finds, giving us crazy-long selector chains;
        It moves things around your codebase. Source order is vital in CSS, so moving selectors around your project should always be avoided;
        It obscures the paper-trail. @extend hides a lot of complexity in our Sass.
        Avoid shorthand syntax everywhere
        Typically, we would view shorthand syntax as a benefit because we have fewer keystrokes, fewer lines of code, less data over the wire. However, it comes with a rather troublesome side effect. It often unsets other properties that we never intended to modify. So, always consider the longhand. It might be more keystrokes, it might be more repetitive, it might be less DRY, but it's more accurate. Only write as much as we need and not a single bit more.

        Avoid too many font files
        Maybe the designers handed us too many font files which is a red flag. A website with too many fonts can be chaotic and confusing, so we should only include the necessary fonts for the page. Fonts can take time to load and be applied and when we have too many fonts. By default, font requests are delayed until the render tree is constructed, which can result in delayed text rendering. It is recommended to optimize WebFont loading and rendering.

        Use multiple classes
        Sometimes it's beneficial to add multiple classes to an element. Let's say that we have a <div> "box" that we want to display a warning and we've already a .warning class in our CSS. We can simply add an extra class in the declaration, like so:

        <div class="box warning"></div>
        We can add as many classes as we'd like (space separated) to any declaration.

        Use nested declarations
        Using CSS preprocessor not only adds some useful functions to our toolset, but also helps with code organization. The best example is styles' declaration nesting. In Sass it's possible to nest selector in other selectors, so that we can see what's the relation between them. It's powerful feature, so it can be overused pretty easily. It´s suggested not to go more than 3 levels deep. This rule applies both for selectors specificity and selectors nesting in CSS preprocessors. Going beyond that limit not only increases selector's strength, but also can make reading our code more difficult.

        Use "Margin: 0 auto" to center layouts
        Many beginners can't figure out why we can't simply use float: center; to achieve that centered effect on block-level elements. Unfortunately, we'll need to use the margin: 0 auto; to center divs, paragraphs or other elements in our layout. By declaring that both the left and the right margins of an element must be identical, they have no choice but to center the element within its containing element.

        Use Hex Code instead of Name Color
        It has been pointed out by experts and professionals that when using "hex code", they found that it is faster for 4-5 runs. Try a performance test run and check for yourself. So rather than using the "name color", go for "#hex code" instead. Besides that, it´s recommended to use naming conventions for our color variables. Instead of scratching our head about this one every time, we can use Veli's colorpedia. This way we'll get to give our colors names that a human can understand.

        Use a CSS reset
        Applying a reset stylesheet should be the first step in any app design. There are several widely-used reset stylesheets available, but the job of each one is the same. It must standardize the differences between different browsers' default styles and to create a clean slate on which to build our app's design. To use a CSS reset, all we need to do is include the reset stylesheet file into our web app before applying any other styles.

        Use a CSS pre-processor
        Part of the reason that CSS can be difficult to work with is that it lacks many of the standard tools available in every programming language. For example, there's no way in CSS to specify variables. It´s recommended to replace CSS with a CSS pre-processor, such as Sass. Pre-processors extend CSS with variables, operators, interpolations, functions, mixins and many more other usable assets. These features make the CSS structure more readable and easier to maintain.

        Use a CSS post-processor
        If feel that there is something wrong while the CSS codes get loaded over the browsers and it seems to be lagging in speed, then there is high time we tried to compress the size of the CSS files. A lot of elements, including line breaks, white spaces, and even redundant CSS styles might be interfering with our CSS file and delaying our app from loading quicker. Code minification and compression are often used interchangeably, maybe because they both address performance optimizations that lead to size reductions. Some of the tools that we can use to get rid of these issues include PostCSS, cssnano and clean-css.

        Use a CSS framework
        A CSS framework, such as Bootstrap, collects together frequently applied styles into a single stylesheet and implements all of the above best practices for us so that we can spend more time thinking about how to improve the website, rather than on making the CSS more manageable. As with any tools, CSS frameworks aren't always right for every job, and they can have bad side effects when used incorrectly. But, learning and using a framework saves time and leads to better results in most cases.

        Use a design system
        A design system is a collection of reusable components, guided by clear standards, that can be assembled together to build any number of applications. A design system allows us to build for the future because it allows us to define our general design rules and specifications, follow an organization, modularize, define best practices, etc. The reason it is a future proof strategy is that it is much easier to introduce changes, fix and configure things on a global scale.

        Use relative units
        We should really try to use relative units. Things like em, rem, %, vw, vh, fr, etc. Setting fix values with px and pt should be things for static design although there are cases that call for these value units. The browser is flexible, so should our website and units.

        Use CSS variables
        Variables is one the reasons why people choose pre-processors but they required compiling before use, thus (sometimes), adding an extra layer of complexity. CSS variables are way better because they stick around when loaded in the browser. The support is good and it allows us to create a more flexible and reusable UI, without mentioning it helps us create a more powerful design system and features.

        Write descriptive media queries
        Media queries are the most important part of responsive website development. We can define styles for different resolutions and change layout according to user's device. Due to the many rules' combination, media query can become complex pretty easily. To make media queries more developer-friendly we can assign it's rules to a variable. In Sass it's possible to use string as normal CSS code using the interpolation braces.

        $medium: 768px;
        $screen-medium-wide: 'only screen and (min-width: #{$medium}) and (max-device-aspect-ratio: 9 / 16)';

        @media #{$screen-medium-wide} {
        body {
            font-size: 20px;
        }
        }
        Understand Block vs Inline Elements
        Block elements are elements that naturally clear each line after they're declared, spanning the whole width of the available space. Inline elements take only as much space as they need, and don't force a new line after they're used. Here are the lists of elements that are either inline or block:

        span, a, strong, em, img, br, input, abbr, acronym
        And the block elements:

        div, h1…h6, p, ul, li, table, blockquote, pre, form
        Separate global vs local style
        It is recommended to distinguish which styles are meant for any or a set of HTML selectors vs. those meant for something specific. We should keep all global styles in a separate file (especially when using a preprocessor). Modern front-end frameworks are the building blocks of our applications' UI. As visual elements, styling them is a big part of how applications meet our users, and composes the way our brand and product looks and feels. These frameworks suggest appending specific styles to each component using separate files.

        Minimize expensive properties
        The browsers are super-fast, however, on complex websites, there are some painting issues related to setting box-shadow, border-radius, position, filter, and even width and height, especially for complex animations or repetitive changes. These require the browser to do complex re-calculations and repaint the view again down to every nested child. The "will-change" is used as a performance boost to tell the browser about how a property is expected to change. However, its use is a last resort.

        Style to be responsive or at least adaptive
        We are creating something to go in the browser which means that people will access it in a variety of device types and sizes. We should consider improving the experience for these people by considering responsive design. If the project does not include a responsiveness plan, we should at least try to remain adaptive. Responsive web design is recommended and rewarded by Google.

        Let the content define the size
        Instead of setting the width and height of a button for example, consider setting some padding for spacing and including a max-width instead and max-height instead unless the design calls for a strict size. This approach will reduce layout bugs and create reusable elements.

        Let the parent take care child position
        When styling a component meant to be used in the content flow, let the content and inner spacing define the size and do not include things like position and margin. Let the container where this component will be used to decide the position and how far apart this component is from others. This approach, among other benefits, allows us to create reusable elements.

        Keep HTML semantics
        It is common to find developers who go around changing their HTML to apply a certain style. In general, let the styling to CSS and let the HTML structured in a way that makes sense semantically. There are exceptions to this rule but always ensure that the adopted structure does not go against any HTML semantic rules. Write the HTML first with content in mind, not styling. Then add CSS and try the best before changing the HTML for styling reasons.

        Create the HTML first
        Many designers create their CSS at the same time they create the HTML. It seems logical to create both at the same time, but actually we'll save even more time if we create the entire HTML mockup first. The reasoning behind this method is that we know all the elements of our site layout, but we don't know what CSS we'll need with our design. Creating the HTML layout first allows us to visualize the entire page as a whole and allows us to think of our CSS in a more holistic, top-down manner.

        Combine elements with same styles
        Elements in a stylesheet sometimes share properties. Instead of re-writing previous code, why not just combine them? For example, the h1, h2, and h3 elements might all share the same font and color:

        h1,
        h2,
        h3 {
        font-family: 'Times New Roman', Times, serif;
        }
        We could add unique characteristics to each of these header styles if we wanted (ie. h1 {size: 2.1em;}) later in the stylesheet.

        Modularize the styles
        We do not need to bundle all CSS in one file unless it will be used. If a user lands on the home page, only include the styles for that page, nothing else. We can go so far as to separate style sheets into essential and non-essential styles. Essential styles are those that once the page loads the user sees them and non-essential styles are those for components that remain hidden like dialog and notifications. Elements or components that require user action to be displayed.

        Lazy load stylesheets
        Lazy loading is a technique that defers loading of non-critical resources at page load time. The portion of fonts, images and video in the typical payload of a website can be significant. By default, CSS is treated as a render blocking resource, so the browser won't render any processed content until the CSSOM is constructed. There are many ways to lazy load the CSS files and it is often easier when using bundlers like webpack and playing around with dynamic import. We can create our own JavaScript CSS loader or we can defer non-critical CSS by playing with the <link> tag when including stylesheets in our page.

        Remove unused CSS
        CSS files can easily gain redundant KBs over time. Unused CSS just adds dead weight to our applications and contributes to the growth of web page size, so we want to make sure that we have as little excess code as possible. Aside from slowing down our website's overall performance, excess CSS can cause headaches for developers. Clean and orderly stylesheets are easier to maintain than disorderly ones. We can remove unused CSS manually or with tools. The most popular tools are PurifyCSS, PurgeCSS and UnCSS.

        Minimize the CSS
        Before loading the CSS into the browser, minimize it. We can use a post-processor or make it a simple build process step of our site deployment. Smaller CSS file will load faster and start to be processed sooner. We can use tools such as cssnano or clean-css. It can also be integrated with a webpack plugin. It uses cssnano to optimize and minify our CSS.
    """,   
]