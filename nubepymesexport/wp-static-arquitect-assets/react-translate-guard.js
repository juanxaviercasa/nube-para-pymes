/**
 * Universal Google Translate / Browser Translation DOM Mutation Guard
 * Prevents React 18/19 crashes ("NotFoundError: Failed to execute 'removeChild' on 'Node'")
 * caused when translation tools wrap text nodes inside <font> tags.
 */
(function() {
  'use strict';
  if (typeof Node === 'function' && Node.prototype) {
    var origRemoveChild = Node.prototype.removeChild;
    Node.prototype.removeChild = function(child) {
      if (child.parentNode !== this) {
        if (child.parentNode) {
          return child.parentNode.removeChild(child);
        }
        return child;
      }
      return origRemoveChild.apply(this, arguments);
    };

    var origInsertBefore = Node.prototype.insertBefore;
    Node.prototype.insertBefore = function(newNode, referenceNode) {
      if (referenceNode && referenceNode.parentNode !== this) {
        if (referenceNode.parentNode) {
          return referenceNode.parentNode.insertBefore(newNode, referenceNode);
        }
        return newNode;
      }
      return origInsertBefore.apply(this, arguments);
    };
  }
})();
