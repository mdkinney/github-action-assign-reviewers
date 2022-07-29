==============
TianoCore GitHub Action Assign Reviewers
==============

Assign reviewers from .github/REVIEWERS using CODEOWNERS syntax

License Details
---------------

The majority of the content in the TianoCore open source project uses a
`BSD-2-Clause Plus Patent License <License.txt>`__.

Resources
---------

-  `TianoCore <http://www.tianocore.org>`__
-  `EDK
   II <https://github.com/tianocore/tianocore.github.io/wiki/EDK-II>`__
-  `Getting Started with EDK
   II <https://github.com/tianocore/tianocore.github.io/wiki/Getting-Started-with-EDK-II>`__
-  `Mailing
   Lists <https://github.com/tianocore/tianocore.github.io/wiki/Mailing-Lists>`__
-  `TianoCore Bugzilla <https://bugzilla.tianocore.org>`__
-  `How To
   Contribute <https://github.com/tianocore/tianocore.github.io/wiki/How-To-Contribute>`__
-  `Release
   Planning <https://github.com/tianocore/tianocore.github.io/wiki/EDK-II-Release-Planning>`__

Code Contributions
------------------

To make a contribution to a TianoCore project, follow these steps.

#. Create a change description in the format specified below to
    use in the source control commit log.
#. Your commit message must include your ``Signed-off-by`` signature
#. Submit your code to the TianoCore project using the process
    that the project documents on its web page. If the process is
    not documented, then submit the code on development email list
    for the project.
#. It is preferred that contributions are submitted using the same
    copyright license as the base project. When that is not possible,
    then contributions using the following licenses can be accepted:

-  BSD (2-clause): http://opensource.org/licenses/BSD-2-Clause
-  BSD (3-clause): http://opensource.org/licenses/BSD-3-Clause
-  MIT: http://opensource.org/licenses/MIT
-  Python-2.0: http://opensource.org/licenses/Python-2.0
-  Zlib: http://opensource.org/licenses/Zlib

For documentation:

-  FreeBSD Documentation License
    https://www.freebsd.org/copyright/freebsd-doc-license.html

Contributions of code put into the public domain can also be accepted.

Contributions using other licenses might be accepted, but further
review will be required.

Developer Certificate of Origin
-------------------------------

Your change description should use the standard format for a
commit message, and must include your ``Signed-off-by`` signature.

In order to keep track of who did what, all patches contributed must
include a statement that to the best of the contributor's knowledge
they have the right to contribute it under the specified license.

The test for this is as specified in the `Developer's Certificate of
Origin (DCO) 1.1 <https://developercertificate.org/>`__. The contributor
certifies compliance by adding a line saying

Signed-off-by: Developer Name developer@example.org

where ``Developer Name`` is the contributor's real name, and the email
address is one the developer is reachable through at the time of
contributing.

::

    Developer's Certificate of Origin 1.1

    By making a contribution to this project, I certify that:

    (a) The contribution was created in whole or in part by me and I
        have the right to submit it under the open source license
        indicated in the file; or

    (b) The contribution is based upon previous work that, to the best
        of my knowledge, is covered under an appropriate open source
        license and I have the right under that license to submit that
        work with modifications, whether created in whole or in part
        by me, under the same open source license (unless I am
        permitted to submit under a different license), as indicated
        in the file; or

    (c) The contribution was provided directly to me by some other
        person who certified (a), (b) or (c) and I have not modified
        it.

    (d) I understand and agree that this project and the contribution
        are public and that a record of the contribution (including all
        personal information I submit with it, including my sign-off) is
        maintained indefinitely and may be redistributed consistent with
        this project or the open source license(s) involved.

Sample Change Description / Commit Message
------------------------------------------

::

    From: Contributor Name <contributor@example.com>
    Subject: [Repository/Branch PATCH] Pkg-Module: Brief-single-line-summary

    Full-commit-message

    Signed-off-by: Contributor Name <contributor@example.com>

Notes for sample patch email
````````````````````````````

-  The first line of commit message is taken from the email's subject
   line following ``[Repository/Branch PATCH]``. The remaining portion
   of the commit message is the email's content.
-  ``git format-patch`` is one way to create this format

Definitions for sample patch email
``````````````````````````````````

-  ``Repository`` is the identifier of the repository the patch applies.
    This identifier should only be provided for repositories other than
    ``edk2``. For example ``edk2-BuildSpecification`` or ``staging``.
-  ``Branch`` is the identifier of the branch the patch applies. This
    identifier should only be provided for branches other than
   ``edk2/master``.
    For example ``edk2/UDK2015``,
   ``edk2-BuildSpecification/release/1.27``, or
    ``staging/edk2-test``.
-  ``Module`` is a short identifier for the affected code or
   documentation. For example ``MdePkg``, ``MdeModulePkg/UsbBusDxe``, ``Introduction``, or
    ``EDK II INF File Format``.
-  ``Brief-single-line-summary`` is a short summary of the change.
-  The entire first line should be less than ~70 characters.
-  ``Full-commit-message`` a verbose multiple line comment describing
    the change. Each line should be less than ~70 characters.
-  ``Signed-off-by`` is the contributor's signature identifying them
    by their real/legal name and their email address.
