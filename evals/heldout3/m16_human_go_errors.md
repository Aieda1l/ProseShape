Go’s treatment of errors as values has served us well over the last decade. Although the standard library’s support for errors has been minimal—just the `errors.New` and `fmt.Errorf` functions, which produce errors that contain only a message—the built-in `error` interface allows Go programmers to add whatever information they desire. All it requires is a type that implements an `Error` method:

```go
type QueryError struct {
    Query string
    Err   error
}

func (e *QueryError) Error() string { return e.Query + ": " + e.Err.Error() }
```

Error types like this one are ubiquitous, and the information they store varies widely, from timestamps to filenames to server addresses. Often, that information includes another, lower-level error to provide additional context.

The pattern of one error containing another is so pervasive in Go code that, after extensive discussion, Go 1.13 added explicit support for it. This post describes the additions to the standard library that provide that support: three new functions in the `errors` package, and a new formatting verb for `fmt.Errorf`.

Before describing the changes in detail, let’s review how errors are examined and constructed in previous versions of the language.
