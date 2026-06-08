# Learn the basics of web accessibility

> Curso: Build web apps with ASP.NET Core for beginners (aspnet-core-web-app) · Seccion: Build web apps with ASP.NET Core for beginners
> Duracion estimada: 15 min

## Objetivos
- (pendiente de expansion por agente)

## Contenido
## Ensuring web pages are accessible to everyone

Ensuring that your webpage is accessible to all users and all clients is critical. As Tim Berners\-Lee, the creator of the World Wide Web, once said: "The power of the Web is in its universality. Access by everyone regardless of disability is an essential aspect."

As a burgeoning web developer, you believe that learning how to ensure that your pages are accessible early on is important. It's always easier to build a page to be accessible than it is to retrofit it later. If you learn these skills when you first start down the path, they'll become natural. You can then create accessible pages and spot potential pitfalls.

In this module, you'll learn about:

* Tools that users use to browse through webpages.
* Tools that developers use to ensure accessibility.
* Skills for ensuring that your pages are accessible.

Prerequisites:

* A browser
* Basic knowledge of HTML and CSS

---

## Surfing the web with more than a browser

You're probably very familiar with using a browser as a client to browse the web. When you think about designing webpages, you can picture the user experience with this client because you have personal experience with it. But not all users use a browser in the same way, or use a browser at all. To create experiences for all users, you should understand the various tools that people might use when they browse the web.

### Screen readers

One of the best\-known accessibility tools is a [screen reader](https://en.wikipedia.org/wiki/Screen_reader). Screen readers are commonly used clients for people with vision impairments. They're built into most operating systems. As we spend time ensuring that a browser properly conveys the information that we want to share, we must also ensure that a screen reader does the same.

At its most basic, a screen reader reads a page from top to bottom audibly. If your page is all text, the reader conveys the information in a similar way to a browser. Of course, webpages are rarely purely text; they contain links, graphics, color, and other visual components. Care must be taken to ensure that a screen reader can correctly read this information.

Some browsers also have built\-in tools and extensions that can read text aloud or even provide some basic navigational features, such as [these accessibility\-focused Edge browser tools](https://support.microsoft.com/help/4000734/microsoft-edge-accessibility-features). These browser tools are also important accessibility tools, but they function differently from screen readers. They shouldn't be mistaken for screen\-reader testing tools.

Note

Try a screen reader and a browser text reader. On Windows, [Narrator](https://support.microsoft.com/windows/complete-guide-to-narrator-e4397a0d-ef4f-b386-d8ae-c172f109bdb1) is included by default. [JAWS](https://webaim.org/articles/jaws/) and [NVDA](https://www.nvaccess.org/about-nvda/) can also be installed on Windows. On macOS and iOS, [VoiceOver](https://support.apple.com/guide/voiceover/welcome/10) is installed by default.

### Zoom

Another tool that people with vision impairments commonly use is zooming. The most basic type of zooming is static zoom, which is controlled through the keyboard shortcut Ctrl\+Plus sign (\+) or by decreasing screen resolution. This type of zoom resizes the entire page. Using [responsive design](https://developer.mozilla.org/docs/Learn/CSS/CSS_layout/Responsive_Design), where items shift based on the [viewport](https://developer.mozilla.org/docs/Web/CSS/Viewport_concepts), is important to provide a good user experience at increased zoom levels.

Your operating system likely has built\-in zoom capabilities that allow you to magnify parts of the screen, much like using a real magnifying glass. [Magnifier](https://support.microsoft.com/windows/use-magnifier-to-make-things-on-the-screen-easier-to-see-414948ba-8b1c-d3bd-8615-0e5e32204198) is built into Windows, whereas [ZoomText](https://www.freedomscientific.com/training/zoomtext/getting-started/) is available as a more fully featured and popular partner add\-on. Both macOS and iOS have a built\-in magnification tool called [Zoom](https://www.apple.com/accessibility/mac/vision/).

---

## Ensuring accessibility with developer tools

Testing your webpage in various clients and views is as important as testing it in various browsers. This testing might not be practical in all scenarios, and it can miss situations where users use a browser but might have another disability. Fortunately, there are tools that you can use as a developer to gauge the accessibility of your page.

### Contrast checkers

Someone who is color\-blind might not be able to differentiate between colors, or might have difficulty working with colors that are similar to one another. The World Wide Web Consortium (W3C), the standards organization for the web, established a [rating system for color contrast](https://www.w3.org/TR/UNDERSTANDING-WCAG20/visual-audio-contrast-contrast.html).

Choosing the right colors to ensure that your page is accessible to all can be tricky to do by hand. You can use the following tools to both generate appropriate colors and test your site to ensure compliance:

* Palette generation tools:
	+ [Adobe Color](https://color.adobe.com/create/color-accessibility), an interactive tool for testing color combinations
	+ [Color Safe](http://colorsafe.co/), a tool for generating text colors based on a selected background color
* Compliance checkers:
	+ Browser extensions to test a page:
		- [Edge: WCAG Color contrast checker](https://microsoftedge.microsoft.com/addons/detail/wcag-color-contrast-check/idahaggnlnekelhgplklhfpchbfdmkjp)
		- [Firefox: WCAG Contrast checker](https://addons.mozilla.org/firefox/addon/wcag-contrast-checker/)
		- [Chrome: Colour Contrast Checker](https://chrome.google.com/webstore/detail/colour-contrast-checker/nmmjeclfkgjdomacpcflgdkgpphpmnfe)
	+ Applications:
		- [Colour Contrast Analyser (CCA)](https://www.tpgi.com/color-contrast-checker/)

### Lighthouse

Lighthouse is a tool that Google created for analyzing websites. It has become so popular that it's included in many browsers' developer tools. Lighthouse can examine a page's search engine optimization (SEO), load performance, and other best practices. Lighthouse can also analyze a page and provide a score for its current accessibility.

Note

As with any automated tool, you can't rely on the score that Lighthouse provides as the sole indication of a page's accessibility. But it does provide a good starting point for identifying and remedying problems.

#### Exercise: Generate a page's Lighthouse accessibility score

Test out Lighthouse in your browser. The following screenshots use [Edge](https://www.microsoft.com/edge), but you can follow the same steps in Chrome and many other browsers.

1. Open your browser and go to the [main Microsoft webpage](https://microsoft.com).
2. Select the `F12` key to open the developer tools.
3. On the top, select the chevron (**\>\>**) icon to open the list of hidden tabs.
4. Select **Lighthouse** from the list.
5. Under **Categories**, clear all items except **Accessibility**.
6. Under **Device**, select **Desktop**.
7. Select **Generate report**.
8. Notice the score and associated information about the page.
9. You can test other pages by selecting **Clear all** in Lighthouse, going to a different page, and then selecting **Generate report**.

You've now seen how to use Lighthouse, along with the accessibility information that the tool can provide.

---

## Ensuring links and images are accessible

Two of the most common components on any webpage are links and images. These items have a profound impact on accessibility. Ensuring good link text and alt text is one of the first steps that you can take to improve your pages for all users.

### Link text

Hyperlinks are core to browsing the web. Ensuring that a screen reader can properly read links allows all users to browse through your site.

Consider the two links in the following example text:

* "The little penguin, sometimes known as the fairy penguin, is the smallest penguin in the world. [Click here](https://en.wikipedia.org/wiki/Little_penguin) for more information."
* "The little penguin, sometimes known as the fairy penguin, is the smallest penguin in the world. Visit <https://en.wikipedia.org/wiki/Little_penguin> for more information."

Note

The two examples demonstrate what you should *not* use as a web developer.

Although these links might seem fine for someone with full sight, they won't work as you might expect with a screen reader. Remember, screen readers read the text. If a URL appears in the text, the screen reader will read the URL. In general, the URL does not convey meaningful information and can sound annoying. You might have experienced this problem if your phone has ever audibly read a text message with a URL.

Screen readers also have the ability to read only the hyperlinks on a page, much in the same way that a sighted person would scan a page for links. If the link text is always "click here", all the user will hear is "click here, click here, click here, click here, click here, ..." All links are now indistinguishable from one another, which is a frustrating experience.

The word "click" is also a problem, because not all users will click. Phone users will tap, keyboard users might select the Enter key or the Spacebar, and other clients will use other means.

We need to always use meaningful link text. Good link text briefly describes what's on the other side of the link. In the earlier example about little penguins, the link goes to the Wikipedia page about the species. The phrase *little penguins* would be perfect link text because it makes it clear what someone will learn about if they select the link:

* "The [little penguin](https://en.wikipedia.org/wiki/Little_penguin), sometimes known as the fairy penguin, is the smallest penguin in the world."

Note

As a bonus for ensuring that your site is accessible to all, you'll also help search engines browse through your site. Search engines use link text to learn the topics of pages. So using good link text helps everyone!

#### ARIA attributes

Imagine the following product page:

| Product | Description | Order |
| --- | --- | --- |
| Widget | `[Description]('#')` | `[Order]('#')` |
| Super widget | `[Description]('#')` | `[Order]('#')` |

This is a common layout for a page that shows information about various items in a table, with links to the description and order. Duplicating the text of description and order make sense for someone who's using a browser. However, someone who's using a screen reader would only hear the words *description* and *order* repeated without context.

To support these types of scenarios, HTML supports a set of attributes known as [Accessible Rich Internet Applications (ARIA)](https://developer.mozilla.org/docs/Web/Accessibility/ARIA). You can use these attributes to provide more information to screen readers.

For example, you can use `aria-label` to describe a link when the format of the page doesn't allow you to. The description for *widget* might be set as:

```
<a href="#" aria-label="Widget description">description</a>

```

ARIA has numerous uses beyond adding text for screen readers to read for links. You can use it to describe the roles that certain elements play when semantic HTML isn't available. When you're creating a tree, for example, you can use ARIA roles to describe the interface to a screen reader:

```
<h2 id="tree-label">File Viewer</h2>
<div role="tree" aria-labelledby="tree-label">
  <div role="treeitem" aria-expanded="false" tabindex="0">Uploads</div>
</div>

```

Important

Using semantic markup and good link text as described earlier generally supersedes the use of ARIA. Browsers and screen readers are not the only clients that a user might use, and designing your page to work well for all clients and users should be your main goal.

### Alt text for images

As a general rule, screen readers can't read the contents of an image. Although some might use artificial intelligence, the generated results might not be contextually accurate. Fortunately, ensuring that images are accessible doesn't take much work \- it's what the `alt` attribute is all about. All meaningful images should have an `alt` attribute (known casually as *alt text*) to describe what they are or the information that they're trying to convey.

Images that are purely decorative should have their `alt` attribute set to an empty string: `alt=""`. This setting prevents screen readers from unnecessarily announcing the decorative image.

Note

As you might expect, search engines can't understand what's in an image. They rely on alt text. So once again, ensuring that your page is accessible provides bonuses!

---

## Designing for accessibility

Accessibility is a relatively large topic. We can't cover it completely in a single Learn module. However, there are some core tenets that you'll want to implement in every page you create. Designing an accessible page from the start is always easier than going back to an existing page to make it accessible.

### Use HTML the way it was designed

HTML provides many elements that you can use to create a page, including buttons, links, and form controls. Each of those elements has a set of built\-in functionality, like being clickable, being linkable, or accepting focus.

Note

*Focus* is a web development term that means a control can accept input from a keyboard. A button can accept focus, allowing someone to activate or "click" it by selecting the Spacebar.

With CSS and JavaScript, it's possible to make any element look like any type of control. For example, you can use `<span>` to create a `<button>` element, and `<b>` can become `<a>`. Although this capability provides some shortcuts for styling or laying out your page, it removes the built\-in functionality. Tools like a screen reader won't be able to understand that `<span>` is being used as `<a>`. Someone browsing with a keyboard won't be able to set focus on a `<div>` element that has been programmed to simulate a `<button>` element.

Another HTML element that's often skipped is headers (`<h1>` through `<h6>`). From a visual standpoint, header tags start from largest to smallest text size. This convention leads many developers to forgo header elements and instead stylize `<div>` or other generic elements.

Unfortunately, stylized generic elements convey only visual information rather than structural. Users of screen readers [rely heavily on headings](https://webaim.org/projects/screenreadersurvey8/#finding) to find information and browse through a page. Writing descriptive heading content and using semantic heading tags are important for creating an easily navigable site for users of screen readers.

As a best practice, you should always use the appropriate HTML when creating controls on a page. If you want a hyperlink, use `<a>`, or use `<button>` for a button.

### Use good visual cues

Developers often think about screen readers as the only accessibility tool. However, users might use numerous other tools, or they might not use tools at all. Users who are using the browser will rely on certain visual cues to understand how to interact with your page.

One of the great features of CSS is that it provides complete control over how to display a page, including removing certain display elements. For example, you can remove the outline from a text box or remove the underline from a hyperlink. Unfortunately, removing those types of cues can make it more challenging for someone who depends on them to recognize the type of control.

### Consider the keyboard

Some users can't use a mouse or trackpad/touchpad. Instead, these users rely on keyboard interactions to tab from one element to the next. It's important for your pages to present your content in logical order so a keyboard user can access each interactive element as they move down.

When a user moves through a page by tabbing, focus moves from one control to the next based on the order in which the controls are listed in the HTML source. The controls for your page should be listed in the HTML source in the order in which you expect the page to be browsed, while relying on CSS to lay out the page visually to users.

For example, imagine creating a form with two columns. You'll want to consider what the natural flow is for someone filling out the form, and then list the controls in that order. Then you can use CSS to create the columns and display the controls in their appropriate locations.

Keyboard navigation relies heavily on semantic HTML. Certain controls (like buttons) accept focus, whereas `div` elements don't. If you're re\-creating controls that already exist in HTML, you're making it more difficult for someone to use your page with a keyboard.

Important

Keyboard navigation needs to be tested manually, and you should do it on every page that you create. [WebAIM](https://webaim.org/techniques/keyboard/) has more information about keyboard navigation strategies.

---

## Summary

In this module, we explored the concepts of web accessibility. You learned about:

* Tools that users use to browse through webpages.
* Tools that developers use to ensure accessibility.
* Skills for ensuring that your pages are accessible.

### Challenge

The best way to understand how to make pages accessible, and the impact of the decisions that you make when creating HTML, is to use some of the tools that users use to browse the web.

Move through a couple of pages by using a screen reader. Open a website that has a form and use only your keyboard to complete it. This activity will give you a sense of what some users experience on a daily basis when using the web, and the importance of ensuring that your pages are accessible.

---

### Credits

This module was first published as a lesson in the [Web Development for Beginners](https://github.com/microsoft/Web-Dev-For-Beginners?azure-portal=true) curriculum by Azure Advocates. The author of the original lesson is Christopher Harrison.

---

_Fuente oficial: https://learn.microsoft.com/en-us/training/modules/web-development-101-accessibility/_

## Fuentes
- [Learn the basics of web accessibility](https://learn.microsoft.com/en-us/training/modules/web-development-101-accessibility/?WT.mc_id=api_CatalogApi)
