(setq autoheader-highlights
      '(("[a-zA-Z]*:.*;" . font-lock-builtin-face)
	("!?[_a-zA-Z0-9\.\/]*:" . font-lock-type-face)
	("[ \t]*[\-_a-zA-Z0-9]*;" . font-lock-function-name-face)
        ("-?=?" . font-lock-keyword-face)
	))

(define-derived-mode autoheader-mode fundamental-mode "autoheader"
  "Major mode for editing .conf files."
  (setq font-lock-defaults '(autoheader-highlights)))
