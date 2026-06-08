# Write your first C# code

> Curso: Build web apps with ASP.NET Core for beginners (aspnet-core-web-app) · Seccion: Build web apps with ASP.NET Core for beginners
> Duracion estimada: 27 min

## Objetivos
- (pendiente de expansion por agente)

## Contenido
## Introduction

The C\# programming language allows you to build many types of applications, like:

* Business applications to capture, analyze, and process data
* Dynamic web applications that can be accessed from a web browser
* Games, both 2D and 3D
* Financial and scientific applications
* Cloud\-based applications
* Mobile applications

But how do you begin to write an application?

Applications are all made up of many lines of code that work together to achieve a task. By far, the best way to learn how to code is to *write* code. It's encouraged that you write code along with the exercises in this module and the others in this learning path. Writing code yourself in each exercise and solving small coding challenges will accelerate your learning.

You'll also begin learning small foundational concepts and build on them with continual practice and exploration.

In this module, you'll:

* Write your first lines of C\# code.
* Use two different techniques to print a message as output.
* Diagnose errors when code is incorrect.
* Identify different C\# syntax elements like operators, classes, and methods.

By the end of this module, you'll be able to write C\# code to print a message to the standard output of a console, like the Windows Terminal. These lines of code will give you your first look at the C\# syntax, and immediately provide invaluable insights.

---

## Exercise \- Write your first code

In this first hands\-on exercise, you'll use C\# to print a hallowed programmer's phrase to the standard output of a console.

### Write your first line of code

There's a long\-standing tradition among software developers to print the phrase "Hello World!" to the console output window. As you'll experience, you can learn a lot about programming and the C\# programming language from this simple exercise.

#### Enter code into the C\# Code Editor

A C\# code editor is available to use directly in the browser: [C\# Code Editor](https://microsoftlearning.github.io/c-sharp-minor?azure-portal=true). This editor provides a lightweight environment for writing, running, and testing C\# code without needing to install any software on your local computer.

1. Open the [C\# Code Editor](https://microsoftlearning.github.io/c-sharp-minor?azure-portal=true) in a new browser window or tab.

You can position the browser windows side\-by\-side so that you can refer to these instructions while you work in the C\# Code Editor.
2. Enter this code exactly as it appears into the C\# Code Editor:

```
Console.WriteLine("Hello World!");

```

You'll see an explanation of how and why it works soon. But first, you should experience it running, and ensure you entered it correctly. To do that, you'll run your code.

Note

You might be tempted to select `Copy` and `Run` and skip all the keystrokes. However, there are benefits to typing code yourself. Entering the code yourself reinforces memory and understanding that will help you gain insights that you wouldn't get otherwise.

#### Run your first code

1. Press the ▶️ Run button

The Run button performs two tasks:

	* It compiles your code into an executable format that a computer can understand.
	* It runs your compiled application and, when written correctly, will output `"Hello World!"`.

#### Observe your results

1. In the output console, observe the result of your code. You should get the following output:

```
Hello World!

```

#### What to do if you get an error message

Writing C\# code is an *exercise in precision*. If you type just one character incorrectly, you'll get an error message in the output area when you run the code.

For example, if you were to incorrectly enter a lower\-case `c` in the word `console` like so:

```
console.WriteLine("Hello World!");

```

You'd get the following error message:

```
Error summary:
  CS0103: The name 'console' does not exist in the current context

```

What does this error message mean?

C\# is a case\-sensitive language, meaning that the C\# compiler considers the words `console` and `Console` as different as the words `cat` and `dog`. Sometimes, the error message can be a bit misleading. You'll need to understand the true reason why the error exists, and that comes through learning more about C\#'s syntax.

Similarly, if you used single\-quotation marks (`'`) to surround the literal string `Hello World!` like so:

```
Console.WriteLine('Hello World!');

```

You would get the following error message:

```
Error summary:
  CS1012: Too many characters in character literal

```

You can use the message as a clue as you investigate the problem. But what does the error message mean? What exactly is a "character literal?" Later, you'll learn more about literals of various data types (including character literals). For now, be careful when you're entering code.

Fortunately, errors are never permanent. You merely spot the error, fix it, and rerun your code.

If you got an error when you ran your code, take a moment to look at it closely. Examine each character and make sure you entered this line of code exactly.

Note

The code editor is constantly monitoring the code you write by performing pre\-compilation to find potential errors. It will try to help you by adding red squiggly lines underlining the code that will produce an error.

Common mistakes new programmers make:

* Entering lower\-case letters instead of capitalizing `C` in `Console`, or the letters `W` or `L` in `WriteLine`.
* Entering a comma instead of a period between `Console` and `WriteLine`.
* Forgetting to use double\-quotation marks, or using single\-quotation marks to surround the phrase `Hello World!`.
* Forgetting a semi\-colon at the end of the command.

Each of these mistakes prevents your code from compiling successfully.

The code editor highlights pre\-compilation errors to help you easily identify and correct mistakes as you develop your code. You can think of it like a spell\-checker that helps you fix grammar or spelling errors in a document.

Assuming you were successful in the previous steps, let's continue.

#### Display a new message

In this task, you'll comment out the previous line of code, then add new lines of code in the .NET Editor to print a new message

1. Modify the code you wrote so that it's prefixed by a code comment using two forward slashes `//`:

```
// Console.WriteLine("Hello World!");

```

You can create a code comment by prefixing a line of code with two forward slashes `//`. This prefix instructs the compiler to ignore all the instructions on that line.

Code comments are helpful when you're not ready to delete the code yet, but you want to ignore it for now. You can also use code comments to add messages to yourself or others who may later read the code, reminding you of what the code is doing.
2. Add new lines of code to match the following code snippet:

```
Console.Write("Congratulations!");
Console.Write(" ");
Console.Write("You wrote your first lines of code.");

```
3. Press the ▶️ Run button again. This time, you should get the following output.

```
Congratulations! You wrote your first lines of code.

```

#### The difference between Console.Write and Console.WriteLine

The three new lines of code you added demonstrated the difference between the [Console.WriteLine()](/en-us/dotnet/api/system.console.writeline#system-console-writeline) and [Console.Write](/en-us/dotnet/api/system.console.write) methods.

`Console.WriteLine()` prints a message to the output console. At the end of the line, it adds a line feed similar to pressing Enter or Return to create a new line.

To print to the output console, but without adding a line feed at the end, you use the second technique, `Console.Write()`. So, the next call to `Console.Write()` prints another message to the same line.

#### Update the message

1. Update your code to match the following code snippet:

```
Console.WriteLine("Congratulations!");
Console.Write("You wrote your first lines of code.");

```
2. Press the ▶️ Run button again. This time, you should get the following output.

```
Congratulations!
You wrote your first lines of code.

```

This code helps demonstrate the difference between the two methods. A new line is appended by `Console.WriteLine()`, and `Console.Write()` prints the output on the current line.

Congratulations on writing your first lines of code!

---

## Learn how it works

To understand how your code works, you need to step back and think about what a programming language is. Consider how your code communicates commands to the computer.

### What is a programming language?

Programming languages like C\# let you write instructions that you want the computer to carry out. Each programming language has its own syntax, but after learning your first programming language and attempting to learn another one, you'll quickly realize that they all share many similar concepts. A programming language's job is to allow a human to express their intent in a human\-readable and understandable way. The instructions you write in a programming language are called "source code" or just "code". Software developers write code.

At this point, a developer can update and change the code, but the computer can't understand the code. The code first must be *compiled* into a format that the computer can understand.

### What is compilation?

A special program called a **compiler** converts your source code into a different format that the computer's central processing unit (CPU) can execute. When you used the ▶️ Run button in the previous unit, the code you wrote was first compiled, then executed.

Why does code need to be compiled? Although most programming languages seem cryptic at first, they can be more easily understood by humans than the computer's *preferred* language. The CPU understands instructions that are expressed by turning thousands or millions of tiny switches either on or off. Compilers bridge these two worlds by translating your human\-readable instructions into a computer\-understandable set of instructions.

### What is syntax?

The rules for writing C\# code is called syntax. Just like human languages have rules regarding punctuation and sentence structure, computer programming languages also have rules. Those rules define the keywords and operators of C\# and how they are put together to form programs.

When you wrote code into the .NET Editor, you may have noticed subtle changes to the color of different words and symbols. Syntax highlighting is a helpful feature that you'll begin to use to easily spot mistakes in your code that don't conform to the syntax rules of C\#.

### How did your code work?

Let's focus on the following line of code you wrote:

```
Console.WriteLine("Hello World!");

```

When you ran your code, you saw that the message `Hello World!` was printed to the output console. When the phrase is surrounded by double\-quotation marks in your C\# code, it's called a **literal string**. In other words, you literally wanted the characters `H`, `e`, `l`, `l`, `o`, and so on, sent to the output.

The `Console` part is called a **class**. Classes "own" methods; or you could say that methods live inside of a class. To visit the method, you must know which class it's in. For now, think of a class as a way to represent an object. In this case, all of the methods that operate on your output console are defined inside of the `Console` class.

There's also a dot (or period) that separates the class name `Console` and the method name `WriteLine()`. The period is the *member access operator*. In other words, the dot is how you "navigate" from the class to one of its methods.

The `WriteLine()` part is called a **method**. You can always spot a method because it has a set of parentheses after it. Each method has one job. The `WriteLine()` method's job is to write a line of data to the output console. The data that's printed is sent in between the opening and closing parenthesis as an input parameter. Some methods need input parameters, while others don't. But if you want to invoke a method, you must always use the parentheses after the method's name. The parentheses are known as the *method invocation operator*.

Finally, the semicolon is the *end of statement operator*. A **statement** is a complete instruction in C\#. The semicolon tells the compiler that you've finished entering the command.

Don't worry if all of these ideas and terms don't make sense. For now, all you need to remember is that if you want to print a message to the output console:

* Use `Console.WriteLine("Your message here");`
* Capitalize `Console`, `Write`, and `Line`
* Use the correct *punctuation* because it has a special role in C\#
* If you make a mistake, just spot it, fix it and re\-run

Tip

Create a cheat sheet for yourself until you've memorized certain key commands.

### Understand the flow of execution

It's important to understand the flow of execution. In other words, your code instructions were executed in order, one line at a time, until there were no more instructions to execute. Some instructions will require the CPU to wait before it can continue. Other instructions can be used to change the flow of execution.

Now, let's test what you've learned. Each module features a simple challenge, and if you get stuck, you'll be supplied with a solution. In the next unit, you'll get a chance to write some C\# on your own.

### Check your knowledge

---

## Complete the challenge

Code challenges throughout these modules will reinforce what you've learned and help you gain some confidence before continuing on.

#### Challenge: Write code in the C\# Code Editor to display two messages

1. Select all of the code in the [C\# Code Editor](https://microsoftlearning.github.io/c-sharp-minor?azure-portal=true), and press `Delete` or `Backspace` to delete it.
2. Write code that produces the following output:

```
This is the first line.
This is the second line.

```

In the previous unit, you learned how to display a message in just one line of code, and you learned how to display a message using multiple lines of code. Use both techniques for this challenge. It doesn't matter which technique you apply to which line, and it doesn't matter how many ways you split one of the messages into multiple lines of code. That's your choice.

No matter how you do it, your code should produce the specified output.

Whether you get stuck and need to peek at the solution or you finish successfully, continue to the next unit to view a solution to this challenge.

---

## Summary

Your goal was to write code that displayed simple messages to an output console while familiarizing yourself with the syntax. You wrote your first lines of code using basic C\# syntax. You learned two techniques for displaying literal\-string data to the console. You also learned what to look for when you come across an error in your code. And lastly, you identified C\# syntax elements like classes and methods, and the purpose of several special symbols that are known as operators. You've taken your first steps towards building more sophisticated applications.

### Get a free verified certification

Microsoft and freeCodeCamp.org offer a training and certification combo on foundational C\#. By completing this Learn module, you're already started. Explore freeCodeCamp's Foundational C\# with Microsoft certification here: [https://aka.ms/csharp\-certification](https://aka.ms/csharp-certification).

---

_Fuente oficial: https://learn.microsoft.com/en-us/training/modules/csharp-write-first/_

## Fuentes
- [Write your first C# code](https://learn.microsoft.com/en-us/training/modules/csharp-write-first/?WT.mc_id=api_CatalogApi)
