(setq autoheader-highlights
      '(("[_a-zA-Z0-9]*:[_a-zA-Z0-9\-\.\/ \t]*;" . font-lock-function-name-face)
	("!?[_a-zA-Z0-9./]*:" . font-lock-type-face)
        ("-?=?" . font-lock-keyword-face)))

(define-derived-mode autoheader-mode fundamental-mode "autoheader"
  "Major mode for editing .conf files."
  (setq font-lock-defaults '(autoheader-highlights)))
